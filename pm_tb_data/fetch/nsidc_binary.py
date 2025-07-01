from pathlib import Path

import numpy as np
import numpy.typing as npt

from pm_tb_data._types import Hemisphere


def read_binary_tb_file(
    *,
    filepath: Path,
    hemisphere: Hemisphere,
) -> npt.NDArray[np.float64]:
    """Read 25km NSIDC binary data from disk.

    Returns data in Kelvins. No/missing data areas are masked with `np.nan`.
    """
    grid_shape = dict(
        north=(448, 304),
        south=(332, 316),
    )[hemisphere]

    try:
        tb_data = np.fromfile(filepath, np.dtype("<i2")).reshape(grid_shape)
    except ValueError as e:
        # TODO: we want a log statement and a warning here!
        # NOTE: This occurs for file:
        # /projects/DATASETS/nsidc0007_smmr_radiance_seaice_v01/TBS/1985/AUG/850804S.37H
        print(f"ValueError trying to read from binary file\n{e}")
        print(f"file: {filepath}")
        tb_data = np.zeros(grid_shape, np.dtype("<i2"))

    # Radiances are in 0.1 kelvins, stored as 2-byte integers, with the least
    # significant byte (lsb) first (lower address) and msb second (higher
    # address). Thus, a value of 1577 represents a Tb of 157.7 kelvins.
    tb_data_kelvins = tb_data * 0.1

    # Mask out values of 0 (missing data):
    tb_data_kelvins[tb_data == 0] = np.nan

    return tb_data_kelvins
