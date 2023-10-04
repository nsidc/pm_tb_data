"""Assess access options for NRT AMSR2 LANCE data."""
import os

import earthaccess
import requests

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
def _download_lance_files():
    results = earthaccess.search_data(short_name="AU_SI12_NRT_R04")
    results = sorted(results, key=lambda x: x["meta"]["revision-date"], reverse=True)

    for granule in results:
        # There are two links for each granule. one for lance.nsstc.nasa.gov and
        # the other for lance.itsc.uah.edu. The first one is fine.
        url = granule.data_links(access="external")[0]
        session = _create_earthdata_authenticated_session(hosts=[url], verify=True)
        with session.get(
            url,
            timeout=60,
            stream=True,
            headers={"User-Agent": "NSIDC-dev-trst2284"},
        ) as resp:
            # e.g., https://lance.nsstc.nasa.gov/.../AMSR_U2_L3_SeaIce12km_P04_20230926.he5
            # -> AMSR_U2_L3_SeaIce12km_P04_20230926.he5
            fn = url.split("/")[-1]
            with open(f"/tmp/test/{fn}", "wb") as f:
                for chunk in resp.iter_content(chunk_size=_CHUNK_SIZE):
                    f.write(chunk)

            print(f"wrote {fn}")


if __name__ == "__main__":
    _download_lance_files()
