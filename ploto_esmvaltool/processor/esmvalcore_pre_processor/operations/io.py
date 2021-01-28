import typing
from pathlib import Path

import iris
import yaml
from esmvalcore._config import get_institutes
from esmvalcore.preprocessor import save, load, concatenate
from esmvalcore.preprocessor._io import concatenate_callback
from loguru import logger
from netCDF4._netCDF4 import Dataset


def run_save(
        operation: typing.Dict,
        task: typing.Dict,
        cubes,
        work_dir: str = ".",
        file_path: typing.Union[str, Path] = None,
        **kwargs
) -> str:
    output_dir = Path(task["output_directory"].format(work_dir=work_dir))
    output_dir.mkdir(parents=True, exist_ok=True)

    project = task["project"]
    dataset = task["dataset"]
    exp = task["exp"]
    ensemble = task["ensemble"]
    short_name = task["short_name"]
    mip = task["mip"]
    start_year = task["start_year"]
    end_year = task["end_year"]

    if file_path is None:
        file_path = Path(
            output_dir,
            f"{project}_{dataset}_{mip}_{exp}_{ensemble}_{short_name}_{start_year}-{end_year}.nc"
        )

    return save(
        cubes=cubes,
        filename=file_path,
        **kwargs
    )


def run_write_metadata(
        operation,
        task: typing.Dict,
        work_dir: typing.Union[Path, str],
        file_path: typing.Union[Path, str],
        metadata_file_name: typing.Union[Path, str]="metadata.yml",
        **kwargs,
) -> Path:
    output_dir = Path(task["output_directory"].format(work_dir=work_dir))
    file_path = Path(file_path).absolute()

    short_name = task["short_name"]

    d = Dataset(file_path)
    field = d[short_name]

    institutes = get_institutes(task)

    dataset = {
        "activity": d.activity_id,
        "alias": task["alias"],
        "dataset": task["dataset"],
        "institute": institutes,
        "ensemble": task["ensemble"],
        "exp": task["exp"],
        "project": task["project"],
        "mip": task["mip"],
        "modeling_realm": task["modeling_realm"],
        "frequency": task["frequency"],
        "grid": task["grid"],
        "start_year": task["start_year"],
        "end_year": task["end_year"],
    }

    variable = {
        "short_name": short_name,
        "long_name": field.long_name,
        "standard_name": field.standard_name,
        "units": field.units,
    }

    diagnostic_task = {
        "variable_group": task["variable_group"],
        "preprocessor": task["preprocessor"],
        "recipe_dataset_index": task["recipe_dataset_index"],
        "diagnostic": task["diagnostic"],
    }

    meta_data = {
        **dataset,
        "filename": str(file_path),
        **variable,
        **diagnostic_task,
    }

    d.close()

    meta_data_path =   Path(output_dir, metadata_file_name)

    with open(meta_data_path, "w") as f:
        yaml.safe_dump({
            str(file_path): meta_data,
        }, f)

    return meta_data_path


def run_load(
        operation: typing.Dict,
        task: typing.Dict,
        cube=None,
        work_dir=".",
        **kwargs
) -> iris.cube.CubeList:
    input_meta_file = task["input_data_source_file"].format(work_dir=work_dir)
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


def run_concatenate(
        operation: typing.Dict,
        task: typing.Dict,
        cube: iris.cube.CubeList,
        **kwargs
) -> iris.cube.Cube:
    cubes = concatenate(cube)
    return cubes
