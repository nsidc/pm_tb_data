import datetime as dt
from pathlib import Path

from pm_tb_data._types import NORTH
from pm_tb_data.fetch.amsr.au_si import get_au_si_tbs

# Directory in which AU_SI12 V3 data is expected to be found.
# NOTE/TODO: This path is specifc to NSIDC infrastructure. Make more generic?
# Fetch data if not present?
DATA_DIR = Path("/ecs/DP1/AMSA/AU_SI12.001/")


def test_get_au_si_tbs():
    date = dt.date(2022, 3, 1)
    tbs = get_au_si_tbs(
        date=date,
        hemisphere=NORTH,
        resolution="12",
    )

    assert "h18" in tbs
