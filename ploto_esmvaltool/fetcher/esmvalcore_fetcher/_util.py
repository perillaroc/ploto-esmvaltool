import pathlib
import typing

from esmvalcore._data_finder import find_files, select_files

from loguru import logger


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

    directories = [pathlib.Path(d, input_dir.format(**dataset)) for d in task["data_path"][project]]
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


def get_native6_data(
        task,
        work_dir,
        config
):
    input_dir = "Tier{tier}/{dataset}/{version}/{frequency}/{short_name}"
    input_file = "*.nc"

    dataset = task["dataset"]
    project = dataset["project"]


    variables = task["variables"]

    files = []
    for v in variables:
        directories = [pathlib.Path(d, input_dir.format(
            **dataset,
            **v,
        )) for d in task["data_path"][project]]
        filenames = input_file.format(**dataset, short_name=v["short_name"])

        files.extend(find_files(
            directories,
            filenames
        ))

    logger.info(f"Found files: {len(files)}")

    selected_files = select_files(
        files,
        start_year=dataset["start_year"],
        end_year=dataset["end_year"]
    )

    return selected_files
