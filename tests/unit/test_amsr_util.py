import numpy as np
import xarray as xr
from xarray.testing import assert_equal

from pm_tb_data._types import NORTH
from pm_tb_data.fetch.amsr.util import normalize_amsr_tbs


def test_normalize_amsr_tbs_au_si():
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
        data_product="AU_SI",
    )

    assert_equal(actual, expected)


def test_normalize_amsr_tbs_ae_si():
    mock_au_si_data_fields = xr.Dataset(
        data_vars={
            "SI_25km_NH_06H_DAY": (
                ("Y", "X"),
                np.arange(0, 6, dtype=np.int16).reshape(2, 3),
            ),
            "SI_25km_NH_89V_DAY": (
                ("Y", "X"),
                np.arange(5, 11, dtype=np.int16).reshape(2, 3),
            ),
        },
    )

    expected_h06 = np.arange(0, 6).reshape(2, 3)
    expected_h06 = expected_h06 / 10.0  # type: ignore[assignment]
    # 0 is missing
    expected_h06[0, 0] = np.nan

    expected_v89 = np.arange(5, 11).reshape(2, 3)
    expected_v89 = expected_v89 / 10.0  # type: ignore[assignment]

    expected = xr.Dataset(
        data_vars={
            "h06": (("fake_y", "fake_x"), expected_h06),
            "v89": (("fake_y", "fake_x"), expected_v89),
        },
    )
    actual = normalize_amsr_tbs(
        data_fields=mock_au_si_data_fields,
        resolution="25",
        hemisphere=NORTH,
        data_product="AE_SI",
    )

    assert_equal(actual, expected)
