"""Code to access DMSP-series data (NSIDC-0001) from NSIDC.

More information about NSIDC-0001: https://nsidc.org/data/nsidc-0001/versions/6

NSIDC-0001 data are provided at two resolutions, depending on the channel:
The 19.3 GHz, 22.2 GHz, and 37.0 GHz data are provided at a resolution of 25 km,
and the 85.5 GHz and 91.7 GHz data are mapped to a 12.5 km grid.
"""
import datetime as dt
import re
from pathlib import Path
from typing import Literal

import xarray as xr

from pm_tb_data._types import NORTH, Hemisphere

NSIDC_0001_RESOLUTIONS = Literal["25", "12.5"]
NSIDC_0001_SATS = Literal["F08", "F11", "F13", "F17", "F18"]


def get_nsidc_0001_fp_on_disk(
    *,
    data_dir: Path,
    hemisphere: Hemisphere,
    date: dt.date,
    resolution: NSIDC_0001_RESOLUTIONS,
) -> Path:
    expected_fn = (
        f"NSIDC0001_TB_PS_{hemisphere[0].upper()}{resolution}km_{date:%Y%m%d}_v6.0.nc"
    )
    expected_fp = data_dir / expected_fn

    if not expected_fp.is_file():
        raise FileNotFoundError(
            f"Expected to find 1 data file for NSIDC-0001 for {date:%Y-%m-%d}"
            f" with filepath: {expected_fp}."
        )

    return expected_fp


def _normalize_nsidc_0001_tbs(
    *,
    ds: xr.Dataset,
    sat: NSIDC_0001_SATS,
) -> xr.Dataset:
    var_pattern = re.compile(f"TB_{sat}_" r"(?P<channel>\d{2})(?P<polarization>H|V)")

    tb_data_mapping = {}
    for var in ds.keys():
        if match := var_pattern.match(str(var)):
            tb_data_mapping[
                f"{match.group('polarization').lower()}{match.group('channel')}"
            ] = ds[var]

    normalized = xr.Dataset(tb_data_mapping)

    return normalized


def get_nsidc_0001_tbs_from_disk(
    *,
    date: dt.date,
    hemisphere: Hemisphere,
    data_dir: Path,
    resolution: NSIDC_0001_RESOLUTIONS,
    sat: NSIDC_0001_SATS,
) -> xr.Dataset:
    """Return TB data from NSIDC-0001.

    Note that the TBs returned are resolution-dependent:

    The 19.3 GHz, 22.2 GHz, and 37.0 GHz data are provided at a resolution of 25 km,
    and the 85.5 GHz and 91.7 GHz data are mapped to a 12.5 km grid.
    """
    expected_dir = data_dir / date.strftime("%Y.%m.%d")
    filepath = get_nsidc_0001_fp_on_disk(
        data_dir=expected_dir,
        date=date,
        resolution=resolution,
        hemisphere=hemisphere,
    )
    ds = xr.open_dataset(filepath, group=sat)
    normalized_ds = _normalize_nsidc_0001_tbs(ds=ds, date=date, sat=sat)

    return normalized_ds


if __name__ == "__main__":
    data_dir = Path("/ecs/DP4/PM/NSIDC-0001.006/")
    date = dt.date(2019, 1, 1)
    tbs = get_nsidc_0001_tbs_from_disk(
        date=date, hemisphere=NORTH, data_dir=data_dir, resolution="25", sat="F17"
    )
