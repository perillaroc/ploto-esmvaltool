import typing

import iris
from esmvalcore.cmor.fix import fix_metadata, fix_data


def run_fix_metadata(
        operation: typing.Dict,
        task: typing.Dict,
        cube: iris.cube.CubeList,
        **kwargs
) -> iris.cube.CubeList:
    short_name = task["variable"]["short_name"]
    project = task["dataset"]["project"]
    dataset = task["dataset"]["dataset"]
    mip = task["dataset"]["mip"]
    frequency = task["dataset"]["frequency"]

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
        task: typing.Dict,
        cube: iris.cube.Cube,
        **kwargs
) -> iris.cube.Cube:
    short_name = task["variable"]["short_name"]
    project = task["dataset"]["project"]
    dataset = task["dataset"]["dataset"]
    mip = task["dataset"]["mip"]

    cubes = fix_data(
        cube,
        short_name=short_name,
        project=project,
        dataset=dataset,
        mip=mip
    )
    return cubes
