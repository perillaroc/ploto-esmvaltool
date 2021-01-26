import typing

from esmvalcore.preprocessor import extract_region

from .util import _get_settings


def run_extract_region(
        operation: typing.Dict,
        task: typing.Dict,
        cube,
        **kwargs,
):
    settings = _get_settings(operation, task)
    start_longitude = settings["start_longitude"]
    end_longitude = settings["end_longitude"]
    start_latitude = settings["start_latitude"]
    end_latitude = settings["end_latitude"]

    cubes = extract_region(
        cube,
        start_longitude=start_longitude,
        end_longitude=end_longitude,
        start_latitude=start_latitude,
        end_latitude=end_latitude,
    )

    return cubes
