"""
ESMValTool Fetcher

Get file paths in local file systems.
"""
import pathlib
import typing

import yaml
from esmvalcore._data_finder import find_files, select_files

from ploto.logger import get_logger


logger = get_logger()


def get_data(
        task: typing.Dict,
        work_dir: typing.Union[pathlib.Path, str],
        config: typing.Dict,
):
    dataset = task["dataset"]

    if "type" in dataset:
        dataset_type = dataset["type"]
    else:
        dataset_type = "exp"

    project = dataset["project"]

    if dataset_type == "exp":
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
    else:
        logger.error(f"dataset type is not supported: {dataset_type}")

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


def get_exp_data(
        task: typing.Dict,
        work_dir: typing.Union[pathlib.Path, str],
        config: typing.Dict,
):
    dataset = task["dataset"]
    project = dataset["project"]
    start_year = dataset["start_year"]
    end_year = dataset["end_year"]

    variables = task["variables"]

    directories = task["data_path"][project]

    filenames = [
        f"{v['short_name']}_{dataset['mip']}_{dataset['dataset']}_"
        f"{dataset['exp']}_{dataset['ensemble']}_{dataset['grid']}*.nc"
        for v in variables
    ]

    files = find_files(
        directories,
        filenames
    )

    logger.info(f"Found files: {len(files)}")

    selected_files = select_files(
        files,
        start_year=start_year,
        end_year=end_year
    )

    return selected_files


def get_obs6_data(
        task,
        work_dir,
        config
):
    input_dir = "Tier{tier}/{dataset}"
    input_file = "{project}_{dataset}_{type}_{version}_{mip}_{short_name}[_.]*nc"

    dataset = task["dataset"]
    project = dataset["project"]

    directories = task["data_path"][project]
    variables = task["variables"]

    filenames = [
        input_file.format(**dataset, short_name=v["short_name"])
        for v in variables
    ]

    files = find_files(
        directories,
        filenames
    )

    logger.info(f"Found files: {len(files)}")

    selected_files = select_files(
        files,
        start_year=dataset["start_year"],
        end_year=dataset["end_year"]
    )

    return selected_files
