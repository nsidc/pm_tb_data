"""Code to access AMSR2 data (AU_SI12 and AU_SI12) from NSIDC.

* More information about AU_SI12: https://nsidc.org/data/au_si12/
* More information about AU_SI25: https://nsidc.org/data/au_si25/
"""
import datetime as dt
import re
from pathlib import Path
from typing import Literal

import xarray as xr
from loguru import logger

from pm_tb_data._types import Hemisphere

AU_SI_RESOLUTIONS = Literal["25"] | Literal["12"]
AU_SI_FN_REGEX = re.compile(
    r"AMSR_U2_L3_SeaIce12km_(?P<file_type>P|R)(?P<file_version>.*)_(?P<file_date>\d{8}).he5"
)


def get_au_si_fp_on_disk(
    data_dir: Path,
    date: dt.date,
    resolution: AU_SI_RESOLUTIONS,
) -> Path:
    """Get the filepath to a AU_SI data file on disk."""
    glob_pattern = f"AMSR_U2_L3_SeaIce{resolution}km_*_{date:%Y%m%d}.he5"
    results = tuple(data_dir.glob(f"**/{glob_pattern}"))

    if len(results) != 1:
        raise FileNotFoundError(
            f"Expected to find 1 data file for AU_SI{resolution} for {date:%Y-%m-%d}"
            f" in {data_dir=}. Found {len(results)}."
        )

    return results[0]


def _get_au_si_data_fields(
    *,
    date: dt.date,
    hemisphere: Hemisphere,
    resolution: AU_SI_RESOLUTIONS,
    data_filepath: Path,
) -> xr.Dataset:
    """Return the data fields from the given `data_filepath` as an xr ds.

    Returns an xr dataset of the variables contained in the
    `HDFEOS/GRIDS/{N|S}pPolarGrid{resolution}km/Data Fields` group.
    """
    ds = xr.open_dataset(
        data_filepath,
        group=(
            f"HDFEOS/GRIDS"
            f"/{hemisphere[0].upper()}pPolarGrid{resolution}km"
            "/Data Fields"
        ),
    )

    return ds


def _normalize_au_si_tbs(
    data_fields: xr.Dataset,
    resolution: AU_SI_RESOLUTIONS,
) -> xr.Dataset:
    """Normalize the given AU_SI* Tbs.

    Currently only returns daily average channels.

    Filters out variables that are not Tbs and renames Tbs to the 'standard'
    {channel}{polarization} name. E.g., `SI_25km_NH_06H_DAY` becomes `h06`
    """
    var_pattern = re.compile(
        f"SI_{resolution}km_" r"(N|S)H_(?P<channel>\d{2})(?P<polarization>H|V)_DAY"
    )

    tb_data_mapping = {}
    for var in data_fields.keys():
        if match := var_pattern.match(str(var)):
            tb_data_mapping[
                f"{match.group('polarization').lower()}{match.group('channel')}"
            ] = data_fields[var]

    normalized = xr.Dataset(tb_data_mapping)

    return normalized


def get_au_si_tbs_from_disk(
    *,
    date: dt.date,
    hemisphere: Hemisphere,
    resolution: AU_SI_RESOLUTIONS,
    data_filepath: Path,
) -> xr.Dataset:
    """Access AU_SI brightness temperatures from data files on local disk."""
    data_fields = _get_au_si_data_fields(
        date=date,
        hemisphere=hemisphere,
        resolution=resolution,
        data_filepath=data_filepath,
    )
    tb_data = _normalize_au_si_tbs(data_fields, resolution=resolution)

    return tb_data


def get_au_si_tbs(
    *,
    date: dt.date,
    hemisphere: Hemisphere,
    resolution: AU_SI_RESOLUTIONS,
) -> xr.Dataset:
    """Access NSIDC AU_SI{resolution} data from disk.

    Returns full orbit daily average data TBs.
    """
    # TODO: extract data dir to `seaice_ecdr`. Ultimately this function will
    # probably go away in favor of using the more generic
    # `get_au_si_tbs_from_disk`, which can be used by the `seaice_ecdr`, which
    # will pass in this `data_dir` as an argument.
    data_dir = Path(f"/ecs/DP1/AMSA/AU_SI{resolution}.001/")

    # Look for the data using the expected file structure in
    # `data_dir`. Fallback to a recursive search in the `data_dir` if the data
    # are not in their expected subdir.
    # TODO: is it really need this logic? Can we just always recursively search
    # for the data we want in the given directory? Often we'll want filepaths
    # for a range of dates, so maybe this needs re-thinking anyway.
    expected_dir = data_dir / f"{date:%Y.%m.%d}"
    try:
        data_filepath = get_au_si_fp_on_disk(
            data_dir=expected_dir,
            date=date,
            resolution=resolution,
        )
    except FileNotFoundError:
        logger.warning(
            f"Could not find AU_SI{resolution} data in expected directory"
            f" ({expected_dir})."
            f" Falling back to recursive search in {data_dir=}"
        )
        data_filepath = get_au_si_fp_on_disk(
            data_dir=data_dir,
            date=date,
            resolution=resolution,
        )

    tb_data = get_au_si_tbs_from_disk(
        date=date,
        hemisphere=hemisphere,
        resolution=resolution,
        data_filepath=data_filepath,
    )

    return tb_data
