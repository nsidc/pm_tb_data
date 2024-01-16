import re
from typing import Literal

import numpy as np
import xarray as xr

from pm_tb_data._types import Hemisphere

AMSR_RESOLUTIONS = Literal["25", "12"]


def normalize_amsr_tbs(
    data_fields: xr.Dataset,
    resolution: AMSR_RESOLUTIONS,
    hemisphere: Hemisphere,
    data_product: Literal["AU_SI", "AE_SI"],
) -> xr.Dataset:
    """Normalize the given Tbs from AU_SI* and AE_SI* products.

    Currently only returns daily average channels.

    Filters out variables that are not Tbs and renames Tbs to the 'standard'
    {channel}{polarization} name. E.g., `SI_25km_NH_06H_DAY` becomes `h06`
    """
    var_pattern = re.compile(
        f"SI_{resolution}km_{hemisphere[0].upper()}H_"
        r"(?P<channel>\d{2})(?P<polarization>H|V)_DAY"
    )

    tb_data_mapping = {}

    for var in data_fields.keys():
        if match := var_pattern.match(str(var)):
            # Preserve variable attrs, but rename the variable and it's dims for
            # consistency.

            data_var = data_fields[var]
            if data_product == "AE_SI":
                # AMSR-E TBs are int16 scaled by 10, and use 0 for
                # missing. These variables lack encoding metadata so `xarray`
                # doesn't decode the data for us like it would for AU_SI data.
                assert data_var.dtype == np.int16
                data_int16 = data_var.data
                var_is_missing = data_int16 == 0
                data = data_int16.astype(np.float64) / 10.0
                data[var_is_missing] = np.nan
            elif data_product == "AU_SI":
                # AMSR2 TB values are properly decoded by xarray
                data = data_var.data
            else:
                raise NotImplementedError(f"{data_product=} is not supported.")

            tb_data_mapping[
                f"{match.group('polarization').lower()}{match.group('channel')}"
            ] = xr.DataArray(
                data,
                dims=("fake_y", "fake_x"),
                attrs=data_fields[var].attrs,
            )

    normalized = xr.Dataset(
        tb_data_mapping,
    )

    return normalized
