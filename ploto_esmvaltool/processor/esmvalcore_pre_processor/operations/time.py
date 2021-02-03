import typing

import iris
from esmvalcore.preprocessor import (
    clip_start_end_year,
    climate_statistics,
)

from .util import _get_settings


def run_clip_start_end_year(
        operation: typing.Dict,
        task: typing.Dict,
        cube: iris.cube.Cube,
        **kwargs
) -> iris.cube.Cube:
    start_year = task["dataset"]["start_year"]
    end_year = task["dataset"]["end_year"]
    cube = clip_start_end_year(
        cube,
        start_year=start_year,
        end_year=end_year,
    )
    return cube


def run_climate_statistics(
        operation: typing.Dict,
        task: typing.Dict,
        cube: iris.cube.Cube,
        **kwargs
):
    settings = _get_settings(operation, task)

    # operator = settings["operator"]
    # period = settings["period"]
    # seasons = settings["seasons"]

    cubes = climate_statistics(
        cube,
        **settings
        # operator=operator,
        # period=period,
        # seasons=seasons,
    )

    return cubes
