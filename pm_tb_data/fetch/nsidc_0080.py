"""Code to access Near-Real-Time DMSP data (NSIDC-0080) from NSIDC.

More information about NSIDC-0080: https://nsidc.org/data/nsidc-0080/versions/2
"""

import datetime as dt
import re
from pathlib import Path
from typing import Literal

import earthaccess
import xarray as xr

from pm_tb_data._types import Hemisphere

NSIDC_0080_RESOLUTION = Literal["25", "12.5"]
NSIDC_0080_PLATFORM_ID = Literal["F16", "F17", "F18"]


def get_nsidc_0080_fp_on_disk(
    *,
    data_dir: Path,
    hemisphere: Hemisphere,
    date: dt.date,
    resolution: NSIDC_0080_RESOLUTION,
) -> Path:
    date_subdir = data_dir / f"{date:%Y.%m.%d}"

    expected_fn = (
        "NSIDC0080_TB_PS"
        f"_{hemisphere[0].upper()}{resolution}km"
        f"_{date:%Y%m%d}_v2.0.nc"
    )

    expected_fp = date_subdir / expected_fn

    if not expected_fp.is_file():
        raise FileNotFoundError(
            f"Expected to find 1 data file for NSIDC-0080 for {date:%Y-%m-%d}"
            f" with filepath: {expected_fp}."
        )

    return expected_fp


def _normalize_nsidc_0080_tbs(
    *,
    ds: xr.Dataset,
    hemisphere: Hemisphere,
    platform_id: NSIDC_0080_PLATFORM_ID,
) -> xr.Dataset:
    var_pattern = re.compile(
        f"TB_{platform_id}_{hemisphere[0].upper()}H_"
        r"(?P<channel>\d{2})(?P<polarization>H|V)"
    )

    tb_data_mapping = {}
    for var in ds.keys():
        if match := var_pattern.match(str(var)):
            # Preserve variable attrs, but rename the variable and it's dims for
            # consistency.
            tb_data_mapping[
                f"{match.group('polarization').lower()}{match.group('channel')}"
            ] = xr.DataArray(
                ds[var].isel(time=0),
                dims=("fake_y", "fake_x"),
                attrs=ds[var].attrs,
            )

    normalized = xr.Dataset(tb_data_mapping)

    return normalized


def get_nsidc_0080_tbs_from_disk(
    *,
    hemisphere: Hemisphere,
    date: dt.date,
    resolution: NSIDC_0080_RESOLUTION,
    platform_id: NSIDC_0080_PLATFORM_ID,
    data_dir: Path = Path("/ecs/DP1/PM/NSIDC-0080.002/"),
) -> xr.Dataset:
    filepath = get_nsidc_0080_fp_on_disk(
        data_dir=data_dir,
        hemisphere=hemisphere,
        date=date,
        resolution=resolution,
    )

    # TODO: ideally, we would use datatree here. xarray >2024.9 should have
    # datatree integrated directly.
    ds = xr.open_dataset(filepath, group=platform_id)

    ds = _normalize_nsidc_0080_tbs(
        ds=ds,
        hemisphere=hemisphere,
        platform_id=platform_id,
    )

    return ds


def get_nsidc_0080_tbs(
    *,
    hemisphere: Hemisphere,
    date: dt.date,
    resolution: NSIDC_0080_RESOLUTION,
    platform_id: NSIDC_0080_PLATFORM_ID,
    version: str = "2",
) -> xr.Dataset:
    """Return TB data from NSIDC-0080 using `earthaccess`"""
    expected_fn = (
        "NSIDC0080_TB_PS"
        f"_{hemisphere[0].upper()}{resolution}km"
        f"_{date:%Y%m%d}_v2.0.nc"
    )

    results = earthaccess.search_data(
        short_name="NSIDC-0080",
        version=version,
        cloud_hosted=True,
        granule_name=expected_fn,
    )
    assert len(results) == 1
    granule_result = results[0]
    _earthaccess_granule = earthaccess.open([granule_result])

    # TODO: ideally, we would use datatree here. xarray >2024.9 should have
    # datatree integrated directly.
    ds = xr.open_dataset(_earthaccess_granule[0], group=platform_id)

    ds = _normalize_nsidc_0080_tbs(
        ds=ds,
        hemisphere=hemisphere,
        platform_id=platform_id,
    )

    return ds
