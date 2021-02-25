import typing

from esmvalcore.preprocessor import derive


def run_derive(
        operation: typing.Dict,
        product: typing.Dict,
        cube,
        **kwargs,
):
    product_variable = product["variable"]
    short_name = product_variable["short_name"]
    long_name = product_variable["long_name"]
    units = product_variable["units"]
    cubes = derive(
        cube,
        short_name=short_name,
        long_name=long_name,
        units=units
    )

    # TODO: see preprocess() in preprocessor/__init__.py
    return [cubes]
