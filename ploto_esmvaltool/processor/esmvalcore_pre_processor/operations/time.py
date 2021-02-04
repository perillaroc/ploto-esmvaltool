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


def run_annual_statistics(
        operation: typing.Dict,
        task: typing.Dict,
        cube: iris.cube.Cube,
        **kwargs
):
    settings = _get_settings(operation, task)
    operator = settings["operator"]

    cubes = annual_statistics(
        cube,
        operator=operator
    )
    return cubes


def run_anomalies(
        operation: typing.Dict,
        task: typing.Dict,
        cube: iris.cube.Cube,
        **kwargs
):
    settings = _get_settings(operation, task)

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
