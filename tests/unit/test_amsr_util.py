import numpy as np
import xarray as xr
from xarray.testing import assert_equal

from pm_tb_data._types import NORTH
from pm_tb_data.fetch.amsr.util import normalize_amsr_tbs


def test_normalize_amsr_tbs():
    mock_au_si_data_fields = xr.Dataset(
        data_vars={
            "SI_25km_NH_06H_DAY": (("Y", "X"), np.arange(0, 6).reshape(2, 3)),
            "SI_25km_NH_89V_DAY": (("Y", "X"), np.arange(5, 11).reshape(2, 3)),
        },
    )

    expected = xr.Dataset(
        data_vars={
            "h06": (("fake_y", "fake_x"), np.arange(0, 6).reshape(2, 3)),
            "v89": (("fake_y", "fake_x"), np.arange(5, 11).reshape(2, 3)),
        },
    )
    actual = normalize_amsr_tbs(
        data_fields=mock_au_si_data_fields,
        resolution="25",
        hemisphere=NORTH,
    )

    assert_equal(actual, expected)
