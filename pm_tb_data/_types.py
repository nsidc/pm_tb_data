from dataclasses import dataclass
from typing import Literal

import xarray as xr

Hemisphere = Literal["north", "south"]

NORTH: Hemisphere = "north"
SOUTH: Hemisphere = "south"


@dataclass
class PmTbData:
    tbs: xr.Dataset
    data_source: str
    # TODO: use `pint` to quantify distance?
    # https://github.com/hgrecco/pint
    resolution: int | float
    resolution_units: str
