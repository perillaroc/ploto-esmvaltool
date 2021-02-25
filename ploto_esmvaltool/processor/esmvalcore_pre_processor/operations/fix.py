import typing

import iris
from esmvalcore.cmor.fix import fix_metadata, fix_data


def run_fix_metadata(
        operation: typing.Dict,
        product: typing.Dict,
        cube: iris.cube.CubeList,
        **kwargs
) -> iris.cube.CubeList:
    product_variable = product["variable"]
    short_name = product_variable["short_name"]
    project = product_variable["project"]
    dataset = product_variable["dataset"]
    mip = product_variable["mip"]
    frequency = product_variable["frequency"]

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
        product: typing.Dict,
        cube: iris.cube.Cube,
        **kwargs
) -> iris.cube.Cube:
    product_variable = product["variable"]
    short_name = product_variable["short_name"]
    project = product_variable["project"]
    dataset = product_variable["dataset"]
    mip = product_variable["mip"]

    cubes = fix_data(
        cube,
        short_name=short_name,
        project=project,
        dataset=dataset,
        mip=mip
    )
    return cubes
