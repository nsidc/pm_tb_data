import datetime as dt
from pathlib import Path

import numpy as np

from pm_tb_data._types import NORTH
from pm_tb_data.fetch.amsr.ae_si import get_ae_si_tbs_from_disk

# Directory in which AE_SI12 V3 data is expected to be found.
# NOTE/TODO: This path is specifc to NSIDC infrastructure. Make more generic?
# Fetch data if not present?
DATA_DIR = Path("/ecs/DP4/AMSA/AE_SI12.003/")


def test_get_ae_si_tbs_from_disk():
    date = dt.date(2010, 1, 1)
    tbs = get_ae_si_tbs_from_disk(
        date=date,
        hemisphere=NORTH,
        data_dir=DATA_DIR,
        resolution="12",
    )

    assert "h18" in tbs

    # AE_SI tbs are not decoded by `xarray` automatically. The variables lack
    # the metadata required to do so. By default these TBs are scaled np.int16
    # data. The normalization code properly scales these data to Kelvins and
    # changes the dtype to `np.float64.`
    assert tbs.h18.dtype == np.float64
