import datetime as dt
from pathlib import Path

from pm_tb_data.fetch.amsr.nsidc_0802 import get_nsidc_0802_tbs_from_disk


def test_get_nsidc_0802_tbs_from_disk():
    # TODO: this data path is temporary!
    data_dir = Path("/share/apps/nsidc0802/dev/scotts/output/")
    data = get_nsidc_0802_tbs_from_disk(
        date=dt.date(2025, 1, 1),
        hemisphere="north",
        data_dir=data_dir,
    )

    assert "tb_19h_calibrated" in data.variables
    assert "tb_37h_calibrated" in data.variables

    assert not data["tb_19h_calibrated"].isnull().all()
    assert not data["tb_37h_calibrated"].isnull().all()
