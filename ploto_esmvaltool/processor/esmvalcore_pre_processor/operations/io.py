import typing
from pathlib import Path

import iris
import yaml
from loguru import logger
from netCDF4 import Dataset

from esmvalcore.preprocessor import save, load, concatenate
from esmvalcore.preprocessor._io import concatenate_callback

from esmvalcore._config import (
    get_institutes,
    get_activity,
)

def run_load(
        operation: typing.Dict,
        product: typing.Dict,
        cube=None,
        work_dir=".",
        **kwargs
) -> iris.cube.CubeList:
    product_input = product["input"]
    product_variable = product["variable"
    ]
    if "input_data_source_file" in product_input:
        input_meta_file = product_input["input_data_source_file"].format(
            work_dir=work_dir,
            **product_variable
        )
        with open(input_meta_file, "r") as f:
            m = yaml.safe_load(f)
            input_files = m["input_files"]
    elif "input_metadata_files" in product_input:
        input_files = []
        for input_metadata_file in product_input["input_metadata_files"]:
            with open(input_metadata_file.format(
                    work_dir=work_dir,
                    **product_variable
            ), "r") as f:
                m = yaml.safe_load(f)
                for k in m:
                    input_files.append(k)
    else:
        raise ValueError("input source has not found. Please set input_files or input_data_source_file")

    callback = concatenate_callback

    cubes = []
    for f in input_files:
        logger.info(f"loading file: {f}")
        cube = load(
            f,
            callback
        )

        cubes.extend(cube)
    cube_list = iris.cube.CubeList(cubes)
    return cube_list


def run_concatenate(
        operation: typing.Dict,
        task: typing.Dict,
        cube: iris.cube.CubeList,
        **kwargs
) -> iris.cube.Cube:
    cube = concatenate(cube)
    return cube


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

    if file_path is None:
        file_path = _get_file_path(task, output_dir)

    return save(
        cubes=cubes,
        filename=file_path,
        **kwargs
    )


def _get_file_path(task, output_dir):
    task_dataset = task["dataset"]
    project = task_dataset["project"]
    dataset = task_dataset["dataset"]
    start_year = task_dataset["start_year"]
    end_year = task_dataset["end_year"]
    short_name = task["variable"]["short_name"]

    if project == "CMIP6":
        exp = task_dataset["exp"]
        if isinstance(exp, typing.List) or isinstance(exp, typing.Tuple):
            exp = "-".join(exp)
        ensemble = task_dataset["ensemble"]
        mip = task_dataset["mip"]
        file_path = Path(
            output_dir,
            f"{project}_{dataset}_{mip}_{exp}_{ensemble}_{short_name}_{start_year}-{end_year}.nc"
        )
    elif project in ("OBS6", "obs4mips", "native6"):
        version = task_dataset["version"]
        mip = task_dataset["mip"]
        data_type = task_dataset["type"]
        file_path = Path(
            output_dir,
            f"{project}_{dataset}_{data_type}_{version}_{mip}_{short_name}_{start_year}-{end_year}.nc"
        )
    else:
        logger.error(f"project is not supported: {project}")
        raise ValueError(f"project is not supported: {project}")

    return file_path


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

    task_diagnostic_dataset = task["diagnostic_dataset"]
    task_diagnostic = task["diagnostic"]
    task_dataset = task["dataset"]
    task_variable = task["variable"]

    short_name = task["variable"]["short_name"]

    project = task_dataset["project"]

    d = Dataset(file_path)
    field = d[short_name]

    if project == "CMIP6":
        institutes = get_institutes(task_dataset)
        activity = get_activity(task_dataset)
        exp = task_dataset["exp"]
        if isinstance(exp, typing.List):
            exp = "-".join(exp)

        dataset = {
            "activity": activity,
            "institute": institutes,
            **task_dataset,
            "exp": exp
        }
    elif project == "OBS6":
        dataset = {
            **task_dataset,
        }
    elif project == "native6":
        dataset = {
            **task_dataset
        }
    elif project == "obs4mips":
        dataset = {
            **task_dataset
        }
    else:
        raise ValueError(f"project is not supported: {project}")

    variable = {
        **task_variable,
        "long_name": field.long_name,
        "standard_name": getattr(field, "standard_name", ''),
        "units": field.units,
    }

    diagnostic_task = {
        **task_diagnostic,
        **task_diagnostic_dataset,
    }

    meta_data = {
        "filename": str(file_path),
        **dataset,
        **diagnostic_task,
        **variable,
    }

    d.close()

    meta_data_path = Path(output_dir, metadata_file_name)

    with open(meta_data_path, "w") as f:
        yaml.safe_dump({
            str(file_path): meta_data,
        }, f)

    return meta_data_path
