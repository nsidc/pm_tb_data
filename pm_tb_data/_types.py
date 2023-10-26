from typing import Literal

from pydantic import BaseModel


class Hemisphere(BaseModel):
    name: Literal["north", "south"]

    @property
    def initial(self) -> str:
        return self.name[0].upper()

    def __str__(self) -> str:
        return self.name

    # Allows e.g., `hemisphere[0]`, which would yeld `n` for the northern
    # hemisphere.
    def __getitem__(self, item):
        return self.name[item]


NORTH = Hemisphere(name="north")
SOUTH = Hemisphere(name="south")
