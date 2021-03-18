import typing

from esmvalcore.preprocessor import (
    extract_levels,
    regrid,
    extract_point
)

from .util import _get_settings


def run_extract_levels(
        cube,
        settings: typing.Dict,
        **kwargs,
):
    levels = settings["levels"]
    scheme = settings["scheme"]

    cubes = extract_levels(
        cube=cube,
        levels=levels,
        scheme=scheme,
    )
    return cubes


def run_regrid(
        cube,
        settings: typing.Dict,
        **kwargs,
):
    target_grid = settings["target_grid"]
    scheme = settings["scheme"]
    lat_offset = settings.get("lat_offset", True)
    lon_offset = settings.get("lon_offset", True)

    cubes = regrid(
        cube=cube,
        target_grid=target_grid,
        scheme=scheme,
        lat_offset=lat_offset,
        lon_offset=lon_offset
    )
    return cubes


def run_extract_point(
        cube,
        settings: typing.Dict,
        **kwargs,
):
    latitude = settings["latitude"]
    longitude = settings["longitude"]
    scheme = settings["scheme"]

    result = extract_point(
        cube,
        latitude=latitude,
        longitude=longitude,
        scheme=scheme,
    )
    return result
