import typing

from esmvalcore.preprocessor import derive


def run_derive(
        operation: typing.Dict,
        cube,
        variable: typing.Dict,
        **kwargs,
):
    short_name = variable["short_name"]
    long_name = variable["long_name"]
    units = variable["units"]
    cubes = derive(
        cube,
        short_name=short_name,
        long_name=long_name,
        units=units
    )

    # TODO: see preprocess() in preprocessor/__init__.py
    return [cubes]
