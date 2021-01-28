import typing

import iris
from esmvalcore.cmor.check import cmor_check_metadata, cmor_check_data


def run_cmor_check_metadata(
        operation: typing.Dict,
        task: typing.Dict,
        cube: iris.cube.Cube,
        **kwargs
) -> iris.cube.Cube:
    short_name = task["variable"]["short_name"]
    project = task["dataset"]["project"]
    mip = task["dataset"]["mip"]

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
    short_name = task["variable"]["short_name"]
    frequency = task["dataset"]["frequency"]
    mip = task["dataset"]["mip"]
    project = task["dataset"]["project"]

    cubes = cmor_check_data(
        cube,
        cmor_table=project,
        mip=mip,
        short_name=short_name,
        frequency=frequency
    )
    return cubes
