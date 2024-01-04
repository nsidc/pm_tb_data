import datetime as dt
from pathlib import Path

from pm_tb_data._types import NORTH
from pm_tb_data.fetch.nsidc_0001 import get_nsidc_0001_tbs_from_disk

# Directory in which NSIDC-0001 V6 data is expected to be found.
# NOTE/TODO: This path is specifc to NSIDC infrastructure. Make more generic?
# Fetch data if not present?
DATA_DIR = Path("/ecs/DP4/PM/NSIDC-0001.006/")


def test_get_nsidc_0001_tbs_from_disk():
    date = dt.date(2019, 1, 1)
    tbs = get_nsidc_0001_tbs_from_disk(
        date=date,
        hemisphere=NORTH,
        data_dir=DATA_DIR,
        resolution="25",
        sat="F17",
    )

    assert "h19" in tbs
