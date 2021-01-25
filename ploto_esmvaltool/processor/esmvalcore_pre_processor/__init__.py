import typing
from pathlib import Path

from loguru import logger
import yaml
from esmvalcore._config import get_institutes

from netCDF4 import Dataset

import ploto_esmvaltool.processor.esmvalcore_pre_processor.operations as esmvalcore_operations

def run_processor(
        task: typing.Dict,
        work_dir: str,
        config: typing.Dict,
):
    """

    Parameters
    ----------
    task: dict

    work_dir: str

    config: dict

    """
    logger.info("running processor: esmvalcore_pre_processor")

    operations = task["operations"]

    cube = None
    for step in operations:
        op = step["type"]
        logger.info(f"run step {op}")
        fun = getattr(esmvalcore_operations, f"run_{op}")
        cube = fun(
            operation=step,
            task=task,
            cube=cube,
            work_dir=work_dir,
        )

    # save to workdir
    file_path = esmvalcore_operations.run_save(
        operation={},
        task=task,
        cubes=[cube],
        work_dir=work_dir,
    )
    logger.info(f"write file to {file_path}")

    output_metadata_file_name = task.get("output_metadata_file_name", "metadata.yml")

    metadata = write_metadata(
        task,
        work_dir,
        file_path,
        metadata_file_name=output_metadata_file_name,
    )
    logger.info(f"write metadata to {metadata.absolute()}")

    logger.info("running processor done: esmvalcore_pre_processor")


def write_metadata(
        task: typing.Dict,
        work_dir: typing.Union[Path, str],
        file_path: typing.Union[Path, str],
        metadata_file_name: typing.Union[Path, str]="metadata.yml",
) -> Path:
    output_dir = Path(work_dir, task["output_directory"])
    # output_dir.mkdir(parents=True, exist_ok=True)
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
