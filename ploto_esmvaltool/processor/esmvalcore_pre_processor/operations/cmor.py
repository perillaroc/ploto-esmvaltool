import typing

import iris
from esmvalcore.cmor.check import cmor_check_metadata, cmor_check_data


def run_cmor_check_metadata(
        operation: typing.Dict,
        task: typing.Dict,
        cube: iris.cube.Cube,
        **kwargs
) -> iris.cube.Cube:
    short_name = task["short_name"]
    project = task["project"]
    mip = task["mip"]

    cubes = cmor_check_metadata(
        cube,
        cmor_table=project,
        mip=mip,
        short_name=short_name,
        frequency="day",
    )
    return cubes


def run_cmor_check_data(
        operation: typing.Dict,
        task: typing.Dict,
        cube: iris.cube.Cube,
        **kwargs
) -> iris.cube.Cube:
    short_name = task["short_name"]
    frequency = task["frequency"]
    mip = task["mip"]

    cubes = cmor_check_data(
        cube,
        "CMIP6",
        mip=mip,
        short_name=short_name,
        frequency=frequency
    )
    return cubes
