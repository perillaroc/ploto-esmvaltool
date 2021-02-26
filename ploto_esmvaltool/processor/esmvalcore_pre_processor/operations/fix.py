import typing

import iris
from esmvalcore.cmor.fix import fix_metadata, fix_data


def run_fix_metadata(
        operation: typing.Dict,
        cube: iris.cube.CubeList,
        variable: typing.Dict,
        **kwargs
) -> iris.cube.CubeList:
    short_name = variable["short_name"]
    project = variable["project"]
    dataset = variable["dataset"]
    mip = variable["mip"]
    frequency = variable["frequency"]

    fixed_cubes = fix_metadata(
        cube,
        short_name=short_name,
        project=project,
        dataset=dataset,
        mip=mip,
        frequency=frequency,
    )

    return fixed_cubes


def run_fix_data(
        operation: typing.Dict,
        cube: iris.cube.Cube,
        variable: typing.Dict,
        **kwargs
) -> iris.cube.Cube:
    short_name = variable["short_name"]
    project = variable["project"]
    dataset = variable["dataset"]
    mip = variable["mip"]

    cubes = fix_data(
        cube,
        short_name=short_name,
        project=project,
        dataset=dataset,
        mip=mip
    )
    return cubes
