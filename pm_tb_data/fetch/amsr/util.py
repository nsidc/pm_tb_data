import re
from typing import Literal

import xarray as xr

from pm_tb_data._types import Hemisphere

AMSR_RESOLUTIONS = Literal["25", "12"]


def normalize_amsr_tbs(
    data_fields: xr.Dataset,
    resolution: AMSR_RESOLUTIONS,
    hemisphere: Hemisphere,
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
            tb_data_mapping[
                f"{match.group('polarization').lower()}{match.group('channel')}"
            ] = xr.DataArray(
                data_fields[var].data,
                dims=("fake_y", "fake_x"),
                attrs=data_fields[var].attrs,
            )

    normalized = xr.Dataset(
        tb_data_mapping,
    )

    return normalized
