import datetime as dt
from pathlib import Path

from pm_tb_data.fetch.nsidc_0802 import get_nsidc_0802_tbs_from_disk


def test_get_nsidc_0802_tbs_from_disk():
    data_dir = Path(
        "/disks/sidads_staging/DATASETS/nsidc0739_AS2_nrt_polar_stereo_tbs_v1/"
    )
    data = get_nsidc_0802_tbs_from_disk(
        date=dt.date(2025, 1, 1),
        hemisphere="north",
        data_dir=data_dir,
    )

    assert "h19" in data.variables
    assert not data["h19"].isnull().all()
