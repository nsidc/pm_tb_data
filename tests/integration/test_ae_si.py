import datetime as dt
from pathlib import Path

from pm_tb_data._types import NORTH
from pm_tb_data.fetch.ae_si import get_ae_si_tbs_from_disk

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
