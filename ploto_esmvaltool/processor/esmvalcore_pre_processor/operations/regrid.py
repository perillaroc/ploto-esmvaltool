import typing

from esmvalcore.preprocessor import (
    extract_levels,
    regrid,
)

from .util import _get_settings


def run_extract_levels(
        operation: typing.Dict,
        product: typing.Dict,
        cube,
        **kwargs,
):
    settings = _get_settings(operation, product)

    levels = settings["levels"]
    scheme = settings["scheme"]

    cubes = extract_levels(
        cube=cube,
        levels=levels,
        scheme=scheme,
    )
    return cubes


def run_regrid(
        operation: typing.Dict,
        product: typing.Dict,
        cube,
        **kwargs,
):
    settings = _get_settings(operation, product)

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
