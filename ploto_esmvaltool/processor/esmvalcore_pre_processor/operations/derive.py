import typing

from esmvalcore.preprocessor import derive


def run_derive(
        operation: typing.Dict,
        task: typing.Dict,
        cube,
        **kwargs,
):
    short_name = task["variable"]["short_name"]
    long_name = task["variable"]["long_name"]
    units = task["variable"]["units"]
    cubes = derive(
        cube,
        short_name=short_name,
        long_name=long_name,
        units=units
    )

    # TODO: see preprocess() in preprocessor/__init__.py
    return [cubes]
