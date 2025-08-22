"""Functions for reading NSIDC-0007 v1 data from disk.

NSIDC-0007 is "Nimbus-7 SMMR Polar Gridded Radiances and Sea Ice Concentrations,
Version 1".

More information about NSIDC-0007:
https://nsidc.org/data/nsidc-0007/versions/1#anchor-2
"""

import calendar
import datetime as dt
import re
from pathlib import Path

import xarray as xr

from pm_tb_data._types import Hemisphere
from pm_tb_data.fetch.nsidc_binary import read_binary_tb_file


def get_nsidc_0007_tbs_from_disk(
    *, date: dt.date, hemisphere: Hemisphere, data_dir: Path
) -> xr.Dataset:
    """Return TB data from NSIDC-0007."""
    # This assumes `data_dir` points to the "nsidc0007_smmr_radiance_seaice_v01"
    # directory. E.g., /projects/DATASETS/nsidc0007_smmr_radiance_seaice_v01/.
    expected_dir = (
        data_dir / "TBS" / str(date.year) / calendar.month_abbr[date.month].upper()
    )

    # Get all of the files containing TB data and match the expected format
    # (e.g., the file `800929S.37H` contains Sept. 29, 1980 SH Tbs for the
    # horizontal 37GHz channel.
    fn_glob = f"{date:%y%m%d}{hemisphere[0].upper()}.*"
    results = list(expected_dir.glob(fn_glob))
    if not results:
        raise FileNotFoundError(f"No NSIDC-0007 TBs found for {date=} {hemisphere=}")

    tb_data_mapping = {}
    tb_fn_re = re.compile(r".*\.(?P<channel>\d{2})(?P<polarization>H|V)")
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
