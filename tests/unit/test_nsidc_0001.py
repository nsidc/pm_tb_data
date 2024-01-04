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
