import datetime as dt
from pathlib import Path

import numpy as np
import xarray as xr
from xarray.testing import assert_equal

from pm_tb_data.fetch import nsidc_0001


def test__normalize_nsidc_0001_tbs():
    mock_nsidc_0001_ds = xr.Dataset(
        data_vars={
            "TB_F17_19H": ("x", np.arange(0, 5)),
            "TB_F17_37V": ("x", np.arange(5, 10)),
            "TB_F18_19H": ("x", np.arange(15, 20)),
            "TB_F18_37V": ("x", np.arange(20, 25)),
        },
    )

    expected = xr.Dataset(
        data_vars={
            "h19": ("x", np.arange(0, 5)),
            "v37": ("x", np.arange(5, 10)),
        },
    )
    actual = nsidc_0001._normalize_nsidc_0001_tbs(
        ds=mock_nsidc_0001_ds,
        sat="F17",
    )

    assert_equal(actual, expected)


def test_get_nsidc_0001_fp_on_disk(fs):
    _data_dir = Path("/path/to/data/dir/2019.10.05")
    _fake_files = [
        _data_dir / "NSIDC0001_TB_PS_N25km_20191005_v6.0.nc",
        _data_dir / "NSIDC0001_TB_PS_S25km_20191005_v6.0.nc",
        _data_dir / "NSIDC0001_TB_PS_N12.5km_20191005_v6.0.nc",
        _data_dir / "NSIDC0001_TB_PS_S12.5km_20191005_v6.0.nc",
    ]
    for _file in _fake_files:
        fs.create_file(_file)

    expected_file = _data_dir / "NSIDC0001_TB_PS_N25km_20191005_v6.0.nc"

    actual = nsidc_0001.get_nsidc_0001_fp_on_disk(
        data_dir=_data_dir,
        date=dt.date(2019, 10, 5),
        resolution="25",
        hemisphere="north",
    )

    assert expected_file == actual
