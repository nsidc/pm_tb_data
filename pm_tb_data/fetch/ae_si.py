"""Code to access AMSR-E data (AE_SI12) from NSIDC.

* More information about AE_SI12: https://nsidc.org/data/ae_si12/versions/3
"""
import datetime as dt
from pathlib import Path

import xarray as xr

from pm_tb_data._types import Hemisphere
from pm_tb_data.fetch import au_si


def get_ae_si_tbs_from_disk(
    *,
    date: dt.date,
    hemisphere: Hemisphere,
    data_dir: Path,
    resolution: au_si.AU_SI_RESOLUTIONS,
) -> xr.Dataset:
    """Return TB data from AE_SI12."""
    expected_dir = data_dir / date.strftime("%Y.%m.%d")
    expected_fn = f"AMSR_E_L3_SeaIce{resolution}km_V15_{date:%Y%m%d}.hdf"
    expected_fp = expected_dir / expected_fn

    if not expected_fp.is_file():
        raise FileNotFoundError(
            f"Expected to find 1 data file for AE_SI{resolution} for {date:%Y-%m-%d}"
            f" with filepath: {expected_fp}."
        )

    with xr.open_dataset(
        expected_fp,
        #  Specify the netcdf4 engine. The "h5netcdf" option does not seem to
        #  work. Note that the netcdf4 engine results in a dataset that has all
        #  of the variables (no subgroups)
        engine="netcdf4",
    ) as ds:
        # TODO: extract normalize func to amsr util module? Make it more clear
        # this is used generically for the AU/SI_* products. Need to be careful
        # - not everything from the au_si module can be used for ae_si. E.g.,
        # the data are stored differently and require a different invocation of
        # `xr.open_dataset`
        normalized = au_si._normalize_au_si_tbs(
            data_fields=ds,
            resolution=resolution,
            hemisphere=hemisphere,
        )

    return normalized
