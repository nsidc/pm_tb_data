import datetime as dt
from pathlib import Path

import numpy as np
import xarray as xr
from xarray.testing import assert_equal

from pm_tb_data.fetch import nsidc_0080


def test__normalize_nsidc_0080_tbs():
    mock_nsidc_0080_ds = xr.Dataset(
        data_vars={
            "TB_F17_NH_19H": (("time", "y", "x"), [np.arange(0, 6).reshape(2, 3)]),
            "TB_F17_NH_37V": (("time", "y", "x"), [np.arange(5, 11).reshape(2, 3)]),
            "TB_F18_NH_19H": (("time", "y", "x"), [np.arange(15, 21).reshape(2, 3)]),
            "TB_F18_NH_37V": (("time", "y", "x"), [np.arange(20, 26).reshape(2, 3)]),
        },
    )

    expected = xr.Dataset(
        data_vars={
            "h19": (("fake_y", "fake_x"), np.arange(0, 6).reshape(2, 3)),
            "v37": (("fake_y", "fake_x"), np.arange(5, 11).reshape(2, 3)),
        },
    )
    actual = nsidc_0080._normalize_nsidc_0080_tbs(
        ds=mock_nsidc_0080_ds,
        hemisphere="north",
        platform_id="F17",
    )

    assert_equal(actual, expected)


def test_get_nsidc_0080_fp_on_disk(fs):
    _data_dir = Path("/path/to/data/dir/")
    _fake_files = [
        _data_dir / "2024.09.05" / "NSIDC0080_TB_PS_N25km_20240905_v2.0.nc",
        _data_dir / "2024.09.05" / "NSIDC0080_TB_PS_S25km_20240905_v2.0.nc",
        _data_dir / "2024.09.05" / "NSIDC0080_TB_PS_N12.5km_20240905_v2.0.nc",
        _data_dir / "2024.09.05" / "NSIDC0080_TB_PS_S12.5km_20240905_v2.0.nc",
    ]
    for _file in _fake_files:
        fs.create_file(_file)

    expected_file = _data_dir / "2024.09.05" / "NSIDC0080_TB_PS_N25km_20240905_v2.0.nc"

    actual = nsidc_0080.get_nsidc_0080_fp_on_disk(
        data_dir=_data_dir,
        date=dt.date(2024, 9, 5),
        resolution="25",
        hemisphere="north",
    )

    assert expected_file == actual
