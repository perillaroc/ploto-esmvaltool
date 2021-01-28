import typing

import iris
from esmvalcore.preprocessor import clip_start_end_year


def run_clip_start_end_year(
        operation: typing.Dict,
        task: typing.Dict,
        cube: iris.cube.Cube,
        **kwargs
) -> iris.cube.Cube:
    start_year = task["dataset"]["start_year"]
    end_year = task["dataset"]["end_year"]
    cube = clip_start_end_year(
        cube,
        start_year=start_year,
        end_year=end_year,
    )
    return cube
