import datetime as dt
from pathlib import Path

from pm_tb_data.fetch import au_si


def test_get_au_si_fp_on_disk(fs):
    _data_dir = Path("/path/to/data/dir")
    _fake_files = [
        _data_dir / "AMSR_U2_L3_SeaIce12km_P04_20231005.he5",
        _data_dir / "AMSR_U2_L3_SeaIce12km_P04_20231004.he5",
        _data_dir / "AMSR_U2_L3_SeaIce12km_P04_20231003.he5",
        _data_dir / "AMSR_U2_L3_SeaIce12km_P04_20231002.he5",
    ]
    for _file in _fake_files:
        fs.create_file(_file)

    expected_file = _data_dir / "AMSR_U2_L3_SeaIce12km_P04_20231003.he5"

    actual = au_si.get_au_si_fp_on_disk(
        data_dir=_data_dir,
        date=dt.date(2023, 10, 3),
        resolution="12",
    )

    assert expected_file == actual
