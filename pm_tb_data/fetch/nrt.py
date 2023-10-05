"""Assess access options for NRT AMSR2 LANCE data."""
import datetime as dt
import os
import re
from pathlib import Path

import earthaccess
import requests
from loguru import logger

_URS_COOKIE = "urs_user_already_logged"
_CHUNK_SIZE = 8 * 1024


def _get_earthdata_creds():
    if not os.environ.get("EARTHDATA_USERNAME"):
        raise RuntimeError("Environment variable EARTHDATA_USERNAME must be defined.")
    if not os.environ.get("EARTHDATA_PASSWORD"):
        raise RuntimeError("Environment variable EARTHDATA_PASSWORD must be defined.")

    return (
        os.environ["EARTHDATA_USERNAME"],
        os.environ["EARTHDATA_PASSWORD"],
    )


def _create_earthdata_authenticated_session(s=None, *, hosts: list[str], verify):
    if not s:
        s = requests.session()

    for host in hosts:
        resp = s.get(
            host,
            # We only want to inspect the redirect, not follow it yet:
            allow_redirects=False,
            # We don't want to accidentally fetch any data:
            stream=True,
            verify=verify,
        )
        # Copy the headers so they can be used case-insensitively after the
        # response is closed.
        headers = {k.lower(): v for k, v in resp.headers.items()}
        resp.close()

        redirected = resp.status_code == 302
        redirected_to_urs = (
            redirected and "urs.earthdata.nasa.gov" in headers["location"]
        )

        if not (redirected_to_urs):
            print(f"Host {host} did not redirect to URS -- continuing without auth.")
            return s

        auth_resp = s.get(
            headers["location"],
            # Don't download data!
            stream=True,
            auth=_get_earthdata_creds(),
        )
        resp.close()
        if not (auth_resp.ok and s.cookies.get(_URS_COOKIE) == "yes"):
            msg = f"Authentication with Earthdata Login failed with:\n{auth_resp.text}"
            raise RuntimeError(msg)

        print(f"Authenticated for {host} with Earthdata Login.")

    return s


# TODO: This and the associated functions (`_get_earthdata_creds` and
# `_create_earthdata_authenticated_session`) should be updated/removed to use
# `earthaccess` to authenticate and download files for each granule we're
# interested in.  Currently the files it downloads from CMR do not contain the
# actual data. See associated issue here:
# https://github.com/nsidc/earthaccess/issues/307
def download_lance_files(*, output_dir: Path, overwrite: bool = False) -> list[Path]:
    # TODO: consider using the `temporal=("%Y-%m-%d", "%Y-%m-%d") to narrow
    # results. For now, we want the full result list because we always need to
    # know the latest date (which we always assume is partial, unless it's an
    # `*_R_*` file). Note that the dates passed to `temporal` kwarg are not
    # inclusive.
    results = earthaccess.search_data(short_name="AU_SI12_NRT_R04")

    fn_pattern = re.compile(
        r"AMSR_U2_L3_SeaIce12km_(?P<file_type>P04|R04)_(?P<file_date>\d{8}).he5"
    )
    # TODO: better name/data structure.
    granules_by_date = {}
    for granule in results:
        # The `native-id` of each granule is the filename. E.g.,
        # `AMSR_U2_L3_SeaIce12km_R04_20230930.he5`.
        filename = granule["meta"]["native-id"]
        if not (match := fn_pattern.match(filename)):
            # TODO: custom `pm_tb_data` error
            raise RuntimeError(
                "Found unexpected filename in CMR results (`native-id`)"
                f": {filename}."
            )
        file_type = match.group("file_type")
        file_date_str = match.group("file_date")
        file_date = dt.datetime.strptime(file_date_str, "%Y%m%d").date()
        # There are two links for each granule. one for lance.nsstc.nasa.gov and
        # the other for lance.itsc.uah.edu. The first one is fine.
        data_url = granule.data_links(access="external")[0]
        granules_by_date[file_date] = {
            "file_type": file_type,
            "granule": granule,
            "filename": filename,
            "data_url": data_url,
        }

    dates = sorted(granules_by_date.keys())
    # If the latest date is a partial file, discard it. We don't trust any data
    # files earlier than the second-to-latest, unless the latest is an R04 file.
    if granules_by_date[dates[-1]]["file_type"] == "P04":
        del granules_by_date[dates[-1]]

    urls = [x["data_url"] for x in granules_by_date.values()]
    session = _create_earthdata_authenticated_session(hosts=urls, verify=True)
    output_paths = []
    for granule_by_date in granules_by_date.values():
        filename = granule_by_date["filename"]
        output_path = Path(output_dir / filename)

        if output_path.is_file() and not overwrite:
            logger.info(
                f"Skipped downloading {filename}. Already exists in {output_dir}"
            )
            continue

        with session.get(
            granule_by_date["data_url"],
            timeout=60,
            stream=True,
            headers={"User-Agent": "pm_tb_data"},
        ) as resp:
            output_paths.append(output_path)
            with open(output_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=_CHUNK_SIZE):
                    f.write(chunk)

            logger.info(f"Wrote AMSR2 LANCE data: {output_path}")

    return output_paths


if __name__ == "__main__":
    output_dir = Path("/tmp/lance/")
    output_dir.mkdir(exist_ok=True)
    downloaded_paths = download_lance_files(output_dir=output_dir)
