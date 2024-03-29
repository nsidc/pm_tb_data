import datetime as dt
from pathlib import Path

from pm_tb_data._types import SOUTH
from pm_tb_data.fetch.nsidc_0007 import get_nsidc_0007_tbs_from_disk

DATA_DIR = Path("/projects/DATASETS/nsidc0007_smmr_radiance_seaice_v01/")


def test_get_nsidc_0007_tbs_from_disk():
    tbs = get_nsidc_0007_tbs_from_disk(
        date=dt.date(1980, 9, 29),
        hemisphere=SOUTH,
        data_dir=DATA_DIR,
    )

    assert "h37" in tbs
