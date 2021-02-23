"""
ESMValTool Fetcher

Get file paths in local file systems.
"""
import pathlib
import typing

import yaml

from ploto.logger import get_logger

from ploto_esmvaltool.fetcher.esmvalcore_fetcher._util import (
    get_exp_data,
    get_obs6_data,
    get_native6_data,
    get_obs4mips_data
)

logger = get_logger()


def get_data(
        task: typing.Dict,
        work_dir: typing.Union[pathlib.Path, str],
        config: typing.Dict,
):
    selected_files = get_selected_files(task, work_dir, config)

    logger.info(f"Selected files: {len(selected_files)}")
    for f in selected_files:
        print(f)

    # write to metadata
    output_metadata_path = pathlib.Path(
        task["output_directory"].format(work_dir=work_dir),
        task["output_data_source_file"]
    )

    output_metadata_path.parent.mkdir(parents=True, exist_ok=True)

    data_source = {
        "input_files": [str(f) for f in selected_files]
    }

    with open(output_metadata_path, "w") as f:
        yaml.safe_dump(data_source, f)

    logger.info(f"write data source file: {str(output_metadata_path)}")


def get_selected_files(
        task: typing.Dict,
        work_dir,
        config: typing.Dict
) -> typing.List:
    dataset = task["dataset"]

    if "type" in dataset:
        dataset_type = dataset["type"]
    else:
        dataset_type = "exp"

    project = dataset["project"]

    if dataset_type == "exp" and project == "CMIP6":
        selected_files = get_exp_data(
            task=task,
            work_dir=work_dir,
            config=config
        )
    elif dataset_type == "reanaly" and project == "OBS6":
        selected_files = get_obs6_data(
            task=task,
            work_dir=work_dir,
            config=config
        )
    elif dataset_type == "reanaly" and project == "native6":
        selected_files = get_native6_data(
            task=task,
            work_dir=work_dir,
            config=config
        )
    elif project == "obs4mips":
        selected_files = get_obs4mips_data(
            task=task,
            work_dir=work_dir,
            config=config
        )
    else:
        logger.exception(f"dataset type is not supported: {dataset}")

    return selected_files
