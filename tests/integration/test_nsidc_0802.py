import datetime as dt
from pathlib import Path

from pm_tb_data.fetch.amsr.nsidc_0802 import get_nsidc_0802_tbs_from_disk


def test_get_nsidc_0802_tbs_from_disk():
    data_dir = Path("/disks/sidads_ftp/DATASETS/nsidc0802_polar_stereo_tbs")
    # TODO: this path should be updated to something like
    # `/share/apps/G02202_V6` once created and prototype data are staged there.
    # eventually, the code to handle the prototype 37h data will be replaced
    # with release ov 0802 v2, which will have all the necessary tbs in nc files.
    prototype_37h_data_dir = Path("/home/vagrant/seaice_ecdr/nise_at_tbs")
    data = get_nsidc_0802_tbs_from_disk(
        date=dt.date(2025, 1, 1),
        hemisphere="north",
        data_dir=data_dir,
        prototype_37h_data_dir=prototype_37h_data_dir,
    )

    assert "h19" in data.variables
    assert "h37" in data.variables

    assert not data["h19"].isnull().all()
    assert not data["h37"].isnull().all()
