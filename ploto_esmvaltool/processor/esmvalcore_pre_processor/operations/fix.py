import typing

import iris
from esmvalcore.cmor.fix import fix_metadata, fix_data


def run_fix_metadata(
        operation: typing.Dict,
        task: typing.Dict,
        cube: iris.cube.CubeList,
        **kwargs
) -> iris.cube.CubeList:
    short_name = task["short_name"]
    project = task["project"]
    dataset = task["dataset"]
    mip = task["mip"]

    fixed_cubes = fix_metadata(
        cube,
        short_name=short_name,
        project=project,
        dataset=dataset,
        mip=mip,
    )

    return fixed_cubes


def run_fix_data(
        operation: typing.Dict,
        task: typing.Dict,
        cube: iris.cube.Cube,
        **kwargs
) -> iris.cube.Cube:
    short_name = task["short_name"]
    project = task["project"]
    dataset = task["dataset"]
    mip = task["mip"]

    cubes = fix_data(
        cube,
        short_name=short_name,
        project=project,
        dataset=dataset,
        mip=mip
    )
    return cubes
