from functools import cached_property
from typing import Literal, NewType

import xarray as xr
from pydantic import BaseModel


class ConfigBaseModel(BaseModel):
    """Implements 'faux' immutability and allows usage of `functools.cached_property`.

    Immutability is not 'strict' (e.g., dicts can be mutated) - a
    determined dev can still mutate model instances.

    This version is for Pydantic ~1.9
    """

    class Config:
        # Throw an error if any unexpected attrs are provided. default: 'ignore'
        # TODO: Once the parameters are determined, uncomment this line
        # extra = Extra.forbid

        # https://pydantic-docs.helpmanual.io/usage/models/#faux-immutability
        allow_mutation = False

        # https://github.com/samuelcolvin/pydantic/issues/1241
        # https://github.com/samuelcolvin/pydantic/issues/2763
        keep_untouched = (cached_property,)

        arbitrary_types_allowed = True


class Hemisphere(ConfigBaseModel):
    _instance = None

    name: Literal["north"] | Literal["south"]

    @property
    def short_name(self):
        """Returns 'NH' or 'SH'."""
        return f"{self.name[0].upper()}H"


TbDataSet = NewType("TbDataSet", xr.Dataset)


class GriddedData(ConfigBaseModel):
    data: TbDataSet
    hemisphere: Hemisphere
