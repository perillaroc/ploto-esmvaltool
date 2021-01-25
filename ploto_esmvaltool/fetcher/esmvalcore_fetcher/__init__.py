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
    dataset = task
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

    logger.info(f"Selected files: {len(selected_files)}")
    for f in selected_files:
        print(f)

    # write to metadata
    output_metadata_path = pathlib.Path(
        work_dir,
        task["output_directory"],
        task["output_data_source_file"]
    )

    output_metadata_path.parent.mkdir(parents=True, exist_ok=True)

    data_source = {
        "input_files": [ str(f) for f in selected_files ]
    }

    with open(output_metadata_path, "w") as f:
        yaml.safe_dump(data_source, f)

    logger.info(f"write data source file: {str(output_metadata_path)}")
