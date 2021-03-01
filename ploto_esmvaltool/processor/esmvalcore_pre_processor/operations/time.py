import typing

import iris
from esmvalcore.preprocessor import (
    clip_start_end_year,
    climate_statistics,
    annual_statistics,
    anomalies,
)

from .util import _get_settings


def run_clip_start_end_year(
        cube: iris.cube.Cube,
        variable: typing.Dict,
        **kwargs
) -> iris.cube.Cube:
    start_year = variable["start_year"]
    end_year = variable["end_year"]
    cube = clip_start_end_year(
        cube,
        start_year=start_year,
        end_year=end_year,
    )
    return cube


def run_climate_statistics(
        cube: iris.cube.Cube,
        settings: typing.Dict,
        **kwargs
):
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


def run_annual_statistics(
        cube: iris.cube.Cube,
        settings: typing.Dict,
        **kwargs
):
    operator = settings["operator"]

    cubes = annual_statistics(
        cube,
        operator=operator
    )
    return cubes


def run_anomalies(
        cube: iris.cube.Cube,
        settings: typing.Dict,
        **kwargs
):
    period = settings["period"]
    reference = settings.get("reference", None)
    standardize = settings.get("standardize", False)
    seasons = settings.get("seasons", ('DJF', 'MAM', 'JJA', 'SON'))

    cubes = anomalies(
        cube,
        period=period,
        reference=reference,
        standardize=standardize,
        seasons=seasons
    )
    return cubes
