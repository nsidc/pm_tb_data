"""Code to download and access NRT AMSR2 data (AU_SI12_NRT_R04).

More information about this data product can be found here:
https://cmr.earthdata.nasa.gov/search/concepts/C1886605827-LANCEAMSR2.html
"""
import copy
import datetime as dt
import os
from pathlib import Path
from typing import Literal, TypedDict, cast

import earthaccess
import requests
import xarray as xr
from earthaccess.results import DataGranule
from loguru import logger

from pm_tb_data._types import Hemisphere
from pm_tb_data.fetch import au_si
from pm_tb_data.fetch.errors import FetchRemoteDataError

EXPECTED_LANCE_AMSR2_FILE_VERSION = "04"
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


# TODO: move to `au_si.py`?
FileType = Literal["R", "P"]


class GranuleInfo(TypedDict):
    file_type: FileType
    filename: str
    data_url: str


GranuleInfoByDate = dict[dt.date, GranuleInfo]


def _get_granule_info_by_date(*, data_granules: list[DataGranule]) -> GranuleInfoByDate:
    # TODO: better name/data structure.
    granules_by_date: GranuleInfoByDate = {}
    for granule in data_granules:
        # The `native-id` of each granule is the filename. E.g.,
        # `AMSR_U2_L3_SeaIce12km_R04_20230930.he5`.
        filename = granule["meta"]["native-id"]
        if not (match := au_si.AU_SI_FN_REGEX.match(filename)):
            # TODO: custom `pm_tb_data` error
            raise FetchRemoteDataError(
                "Found unexpected filename in CMR results (`native-id`)"
                f": {filename}."
            )

        file_version = match.group("file_version")
        if file_version != EXPECTED_LANCE_AMSR2_FILE_VERSION:
            logger.warning(
                f"Unexpected version in {filename=}."
                f" Expected {EXPECTED_LANCE_AMSR2_FILE_VERSION}."
                f" Got {file_version} instead."
                " Downloading anyway, but downstream code may need to be"
                " updated for this file version."
            )

        file_type = match.group("file_type")
        file_type = cast(FileType, file_type)
        file_date_str = match.group("file_date")
        file_date = dt.datetime.strptime(file_date_str, "%Y%m%d").date()
        # There are two links for each granule. one for lance.nsstc.nasa.gov and
        # the other for lance.itsc.uah.edu. The first one is fine.
        data_url = granule.data_links(access="external")[0]
        granules_by_date[file_date] = {
            "file_type": file_type,
            "filename": filename,
            "data_url": data_url,
        }

    return granules_by_date


def _filter_out_last_day(*, granules_by_date: GranuleInfoByDate) -> GranuleInfoByDate:
    """Remove the last day of data, unless it is an R file."""
    filtered_granules_by_date = copy.deepcopy(granules_by_date)
    dates = sorted(granules_by_date.keys())
    latest_file_date = dates[-1]
    # If the latest date is a partial file, discard it. We don't trust any data
    # files earlier than the second-to-latest, unless the latest is an R file.
    if granules_by_date[latest_file_date]["file_type"] == "P":
        del filtered_granules_by_date[latest_file_date]

    return filtered_granules_by_date


# TODO: This and the associated functions (`_get_earthdata_creds` and
# `_create_earthdata_authenticated_session`) should be updated/removed to use
# `earthaccess` to authenticate and download files for each granule we're
# interested in.  Currently the files it downloads from CMR do not contain the
# actual data. See associated issue here:
# https://github.com/nsidc/earthaccess/issues/307
def download_latest_lance_files(
    *,
    output_dir: Path,
    overwrite: bool = False,
    fail_on_404: bool = False,
) -> list[Path]:
    """Download the latest LANCE AMSR2 data files that are ready for NRT.

    The latest available day of data ready for NRT is the day before the latest
    available file, unless the latest available file is an `R` file.

    NOTE: because of a problem with CMR providing results for ganules that do
    not exist at the specified download location, attempts to fetch data files
    that result in a 404 response code (Not Found) will cause a warning to be
    logged and that granule will be skipped. Setting `fail_on_404=True` will
    cause an HttpError to be raised for these cases instead.

    Returns a list of paths to newly downloaded data.
    """
    # LANCE only has the last 14 days worth of data at any given time. For
    # simplicity, query for all of them.
    results = earthaccess.search_data(short_name="AU_SI12_NRT_R04")

    granules_by_date = _get_granule_info_by_date(data_granules=results)
    filtered_granules_by_date = _filter_out_last_day(granules_by_date=granules_by_date)

    urls = [x["data_url"] for x in filtered_granules_by_date.values()]
    session = _create_earthdata_authenticated_session(hosts=urls, verify=True)
    output_paths = []
    for granule_by_date in filtered_granules_by_date.values():
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
            if resp.status_code == 404 and not fail_on_404:
                # If we receive a 404 response for a granule, log a warning and
                # skip. We have observed this problem starting on Oct. 10,
                # 2023. CMR reports an R file for 2023-10-09, but only a P file
                # exists. This issue was raised on the earthdata forum, but
                # cannot be fixed on NSIDC's side.
                logger.warning(
                    "Got a 404 response for granule reported by CMR:"
                    f" url={granule_by_date['data_url']}."
                    " This may be a problem with the LANCE CMR record. Skipping..."
                )
                continue

            resp.raise_for_status()
            output_paths.append(output_path)
            # TODO: it would be ideal to write this to a temp dir, then move it
            # to `output_dir`. Otherwise a failure in downloading the data could
            # result in partially-processed data.
            with open(output_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=_CHUNK_SIZE):
                    f.write(chunk)

            logger.info(f"Wrote AMSR2 LANCE data: {output_path}")

    return output_paths


def access_local_lance_data(
    *,
    date: dt.date,
    data_dir: Path,
    hemisphere: Hemisphere,
) -> xr.Dataset:
    """Access 12.5km LANCE AMSR2 data from local disk.

    Returns full orbit daily average data TBs.
    """
    data_resolution: au_si.AU_SI_RESOLUTIONS = "12"
    data_filepath = au_si.get_au_si_fp_on_disk(
        data_dir=data_dir,
        date=date,
        resolution=data_resolution,
    )

    data_fields = au_si.get_au_si_tbs_from_disk(
        date=date,
        data_filepath=data_filepath,
        hemisphere=hemisphere,
        resolution=data_resolution,
    )

    return data_fields
