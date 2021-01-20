import typing
from pathlib import Path

from esmvalcore.preprocessor import (
    load,
    save,
    fix_metadata,
    concatenate,
    cmor_check_metadata,
    clip_start_end_year,
    fix_data,
    cmor_check_data,
)
from esmvalcore.preprocessor._io import concatenate_callback

import yaml
import iris
from loguru import logger


def run_load(
        operation: typing.Dict,
        task: typing.Dict,
        cube=None,
        **kwargs
) -> iris.cube.CubeList:
    input_meta_file = task["input_meta_file"]
    with open(input_meta_file, "r") as f:
        m = yaml.safe_load(f)
        input_files = m["input_files"]

    callback = concatenate_callback

    cubes = []
    for f in input_files:
        logger.info(f"loading file: {f}")
        cube = load(
            f,
            callback
        )

        cubes.extend(cube)
    return iris.cube.CubeList(cubes)


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


def run_concatenate(
        operation: typing.Dict,
        task: typing.Dict,
        cube: iris.cube.CubeList,
        **kwargs
) -> iris.cube.Cube:
    cubes = concatenate(cube)
    return cubes


def run_cmor_check_metadata(
        operation: typing.Dict,
        task: typing.Dict,
        cube: iris.cube.Cube,
        **kwargs
) -> iris.cube.Cube:
    short_name = task["short_name"]
    project = task["project"]
    mip = task["mip"]

    cubes = cmor_check_metadata(
        cube,
        cmor_table=project,
        mip=mip,
        short_name=short_name,
        frequency="day",
    )
    return cubes


def run_clip_start_end_year(
        operation: typing.Dict,
        task: typing.Dict,
        cube: iris.cube.Cube,
        **kwargs
) -> iris.cube.Cube:
    start_year = task["start_year"]
    end_year = task["end_year"]
    cube = clip_start_end_year(
        cube,
        start_year=start_year,
        end_year=end_year,
    )
    return cube


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


def run_cmor_check_data(
        operation: typing.Dict,
        task: typing.Dict,
        cube: iris.cube.Cube,
        **kwargs
) -> iris.cube.Cube:
    short_name = task["short_name"]
    frequency = task["frequency"]
    mip = task["mip"]

    cubes = cmor_check_data(
        cube,
        "CMIP6",
        mip=mip,
        short_name=short_name,
        frequency=frequency
    )
    return cubes


def run_save(
        operation,
        task: typing.Dict,
        cubes,
        work_dir: str =".",
        **kwargs
) -> str:
    output_dir = Path(work_dir, task["output_directory"])
    output_dir.mkdir(parents=True, exist_ok=True)

    project = task["project"]
    dataset = task["dataset"]
    exp = task["exp"]
    ensemble = task["ensemble"]
    short_name = task["short_name"]
    mip = task["mip"]
    start_year = task["start_year"]
    end_year = task["end_year"]

    file_path = Path(output_dir, f"{project}_{dataset}_{mip}_{exp}_{ensemble}_{short_name}_{start_year}-{end_year}.nc")

    return save(
        cubes=cubes,
        filename=file_path,
        **kwargs
    )
