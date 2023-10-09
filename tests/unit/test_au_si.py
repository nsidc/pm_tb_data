import datetime as dt
from pathlib import Path

import numpy as np
import xarray as xr
from xarray.testing import assert_equal

from pm_tb_data.fetch import au_si


def test__normalize_au_si_tbs():
    mock_au_si_data_fields = xr.Dataset(
        data_vars={
            "SI_25km_NH_06H_DAY": ("x", np.arange(0, 5)),
            "SI_25km_NH_89V_DAY": ("x", np.arange(5, 10)),
        },
    )

    expected = xr.Dataset(
        data_vars={
            "h06": ("x", np.arange(0, 5)),
            "v89": ("x", np.arange(5, 10)),
        },
    )
    actual = au_si._normalize_au_si_tbs(
        data_fields=mock_au_si_data_fields,
        resolution="25",
    )

    assert_equal(actual, expected)


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
