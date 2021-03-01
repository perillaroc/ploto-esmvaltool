import typing

import iris
from esmvalcore.cmor.check import cmor_check_metadata, cmor_check_data


def run_cmor_check_metadata(
        cube: iris.cube.Cube,
        variable: typing.Dict,
        **kwargs
) -> iris.cube.Cube:
    short_name = variable["short_name"]
    project = variable["project"]
    mip = variable["mip"]
    frequency = variable["frequency"]

    cubes = cmor_check_metadata(
        cube,
        cmor_table=project,
        mip=mip,
        short_name=short_name,
        frequency=frequency,
    )
    return cubes


def run_cmor_check_data(
        cube: iris.cube.Cube,
        variable: typing.Dict,
        **kwargs
) -> iris.cube.Cube:
    short_name = variable["short_name"]
    frequency = variable["frequency"]
    mip = variable["mip"]
    project = variable["project"]

    cubes = cmor_check_data(
        cube,
        cmor_table=project,
        mip=mip,
        short_name=short_name,
        frequency=frequency
    )
    return cubes
