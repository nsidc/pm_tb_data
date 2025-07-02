"""Functions to read tbs from NSIDC-0802 binary files.

TODO: link to dataset landing page. Product is currently a prototype, but
expected to be published soon.
"""

import datetime as dt
import re
from pathlib import Path

import xarray as xr

from pm_tb_data._types import Hemisphere
from pm_tb_data.fetch.nsidc_binary import read_binary_tb_file


def get_nsidc_0802_tbs_from_disk(
    *,
    date: dt.date,
    hemisphere: Hemisphere,
    data_dir: Path,
) -> xr.Dataset:
    """Return TB data from NSIDC-0802."""
    # This assumes `data_dir` points to the "nsidc0007_smmr_radiance_seaice_v01"
    # directory. E.g., /projects/DATASETS/nsidc0007_smmr_radiance_seaice_v01/.

    # Get all of the files containing TB data and match the expected format
    # (e.g., the file `800929S.37H` contains Sept. 29, 1980 SH Tbs for the
    # horizontal 37GHz channel.
    fn_glob = f"tb_as2_{date:%Y%m%d}_nrt_{hemisphere[0].lower()}*.bin"
    results = list(data_dir.rglob(fn_glob))
    if not results:
        raise FileNotFoundError(f"No NSIDC-0007 TBs found for {date=} {hemisphere=}")

    tb_data_mapping = {}
    tb_fn_re = re.compile(
        r".*_" + hemisphere[0].lower() + r"(?P<channel>\d{2})(?P<polarization>h|v).bin"
    )
    for tb_fp in results:
        match = tb_fn_re.match(tb_fp.name)
        assert match is not None

        data = read_binary_tb_file(
            filepath=tb_fp,
            hemisphere=hemisphere,
        )

        tb_data_mapping[
            f"{match.group('polarization').lower()}{match.group('channel')}"
        ] = xr.DataArray(
            data,
            dims=("fake_y", "fake_x"),
            attrs={
                "source_filename": tb_fp.name,
            },
        )

    normalized = xr.Dataset(tb_data_mapping)

    return normalized
