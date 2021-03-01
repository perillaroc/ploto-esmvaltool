import typing

from esmvalcore.preprocessor import (
    extract_region,
    area_statistics,
    zonal_statistics,
)


def run_extract_region(
        cube,
        settings: typing.Dict,
        **kwargs,
):
    start_longitude = settings["start_longitude"]
    end_longitude = settings["end_longitude"]
    start_latitude = settings["start_latitude"]
    end_latitude = settings["end_latitude"]

    cubes = extract_region(
        cube,
        start_longitude=start_longitude,
        end_longitude=end_longitude,
        start_latitude=start_latitude,
        end_latitude=end_latitude,
    )

    return cubes

def run_area_statistics(
        cube,
        settings: typing.Dict,
        **kwargs,
):
    operator = settings["operator"]
    fx_variables = None

    cubes = area_statistics(
        cube,
        operator=operator,
        fx_variables=fx_variables
    )
    return cubes


def run_zonal_statistics(
        cube,
        settings,
        **kwargs
):
    operator = settings["operator"]
    return zonal_statistics(
        cube=cube,
        operator=operator,
    )