import datetime as dt
from pathlib import Path

from pm_tb_data.fetch.amsr.nsidc_0802 import get_nsidc_0802_tbs_from_disk


def test_get_nsidc_0802_tbs_from_disk():
    data_dir = Path("/disks/sidads_ftp/DATASETS/nsidc0802_polar_stereo_tbs")
    data = get_nsidc_0802_tbs_from_disk(
        date=dt.date(2025, 1, 1),
        hemisphere="north",
        data_dir=data_dir,
    )

    assert "h19" in data.variables
    assert not data["h19"].isnull().all()
