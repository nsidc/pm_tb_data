"""Functions to read tbs from NSIDC-0802 binary files.

TODO: link to dataset landing page. Product is currently a prototype, but
expected to be published soon.
"""

import datetime as dt
import re
from pathlib import Path

import xarray as xr
from loguru import logger

from pm_tb_data._types import Hemisphere
from pm_tb_data.fetch.nsidc_binary import read_binary_tb_file


def get_nsidc_0802_tbs_from_disk(
    *,
    date: dt.date,
    hemisphere: Hemisphere,
    data_dir: Path,
    prototype_37h_data_dir: Path,
) -> xr.Dataset:
    """Return TB data from NSIDC-0802."""
    # This assumes `data_dir` points to the "nsidc0802_polar_stereo_tbs"
    # directory. E.g., /disks/sidads_ftp/DATASETS/nsidc0802_polar_stereo_tbs/.

    # Example fn: NSIDC-0802_TB_AMSR2_N_37V_20250702_V1.0.bin
    fn_glob = f"NSIDC-0802_TB_AMSR2_{hemisphere[0].upper()}_*_{date:%Y%m%d}_*.bin"
    results = list(data_dir.rglob(fn_glob))
    if not results:
        raise FileNotFoundError(f"No NSIDC-0007 TBs found for {date=} {hemisphere=}")

    # Example fn: tb_as2_20240108_sfm_s37h.dat
    prototype_37h_fn_glob = f"tb_as2_{date:%Y%m%d}_sfm_{hemisphere[0].lower()}37h.dat"
    prototype_37h_results = list(prototype_37h_data_dir.rglob(prototype_37h_fn_glob))
    prototype_37h_fp: None | Path = None
    if len(prototype_37h_results) == 1:
        prototype_37h_fp = prototype_37h_results[0]
    else:
        logger.warning(f"Failed to find 37h data for {date=}")

    tb_data_mapping = {}
    # Published binary files
    tb_fn_re = re.compile(
        r"NSIDC-0802_TB_AMSR2_"
        + hemisphere[0].upper()
        + r"_(?P<channel>\d{2})(?P<polarization>H|V)_.*.bin"
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

    # prototype 37h
    if prototype_37h_fp is not None:
        prototype_37h_data = read_binary_tb_file(
            filepath=prototype_37h_fp,
            hemisphere=hemisphere,
        )

        tb_data_mapping["h37"] = xr.DataArray(
            prototype_37h_data,
            dims=("fake_y", "fake_x"),
            attrs={
                "source_filename": tb_fp.name,
            },
        )

    normalized = xr.Dataset(tb_data_mapping)

    return normalized
