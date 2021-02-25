import typing

import iris
from esmvalcore.cmor.check import cmor_check_metadata, cmor_check_data


def run_cmor_check_metadata(
        operation: typing.Dict,
        product: typing.Dict,
        cube: iris.cube.Cube,
        **kwargs
) -> iris.cube.Cube:
    product_variable = product["variable"]
    short_name = product_variable["short_name"]
    project = product_variable["project"]
    mip = product_variable["mip"]
    frequency = product_variable["frequency"]

    cubes = cmor_check_metadata(
        cube,
        cmor_table=project,
        mip=mip,
        short_name=short_name,
        frequency=frequency,
    )
    return cubes


def run_cmor_check_data(
        operation: typing.Dict,
        product: typing.Dict,
        cube: iris.cube.Cube,
        **kwargs
) -> iris.cube.Cube:
    product_variable = product["variable"]
    short_name = product_variable["short_name"]
    frequency = product_variable["frequency"]
    mip = product_variable["mip"]
    project = product_variable["project"]

    cubes = cmor_check_data(
        cube,
        cmor_table=project,
        mip=mip,
        short_name=short_name,
        frequency=frequency
    )
    return cubes
