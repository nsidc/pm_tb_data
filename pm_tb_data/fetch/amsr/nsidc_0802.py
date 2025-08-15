"""Functions to read tbs from NSIDC-0802 binary files.

TODO: link to dataset landing page. Product is currently a prototype, but
expected to be published soon.

NOTE: most of the data products incldued in `pm_tb_data` "normalize" tb names to
be something like `h19`. This is not currently done with nsidc0802, in part
because there are "calibrated" versions of each channel (e.g.,
`tb_19h_calibrated`). We could drop the `tb_` and remap `19h_` to `h19_`, but it
does not seem necessary for this dataset. The nc dataset is already nicely
formatted and contains all the metadata it needs. Ideally, `pm_tb_data`
structures poorly structured data into a better format, and this one doesn't
really need it.
"""

import datetime as dt
from pathlib import Path

import xarray as xr

from pm_tb_data._types import Hemisphere


def get_nsidc_0802_tbs_from_disk(
    *,
    date: dt.date,
    hemisphere: Hemisphere,
    data_dir: Path,
) -> xr.Dataset:
    """Return TB data from NSIDC-0802."""
    fn_glob = f"NSIDC-0802_TB_AMSR2_{hemisphere[0].upper()}_{date:%Y%m%d}_*.nc"
    results = list(data_dir.rglob(fn_glob))
    if not len(results) == 1:
        raise FileNotFoundError(f"No NSIDC-0007 TBs found for {date=} {hemisphere=}")

    matching_filepath = results[0]
    ds = xr.open_dataset(matching_filepath)

    return ds
