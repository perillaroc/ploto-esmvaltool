import pathlib
import typing
import itertools

from esmvalcore._data_finder import find_files, select_files

from loguru import logger


def get_exp_data(
        task: typing.Dict,
        work_dir: typing.Union[pathlib.Path, str],
        config: typing.Dict,
) -> typing.List:
    """
    由 dataset 和 variable 共同决定数据文件查找的参数 combined_variable
    """
    dataset = task["dataset"]
    project = dataset["project"]

    exp = dataset["exp"]
    if isinstance(exp, str):
        exp = [exp]

    ensemble = dataset["ensemble"]
    if isinstance(ensemble, str):
        ensemble = [ensemble]

    variables = task["variables"]

    directories = task["data_path"][project]

    selected_files = []

    iter = itertools.product(exp, ensemble, variables)
    for e, ens, v in iter:
        combined_variable = {
            **dataset,
            **v,
            "exp": e,
            "ensemble": ens
        }
        start_year = combined_variable["start_year"]
        end_year = combined_variable["end_year"]

        logger.info(f"checking for variable {combined_variable}")
        filenames = [
            f"{combined_variable['short_name']}_{combined_variable['mip']}_{combined_variable['dataset']}_"
            f"{combined_variable['exp']}_{combined_variable['ensemble']}_{combined_variable['grid']}*.nc"
        ]

        files = find_files(
            directories,
            filenames
        )

        logger.info(f"Found files: {len(files)}")

        current_selected_files = select_files(
            files,
            start_year=start_year,
            end_year=end_year
        )

        selected_files.extend(current_selected_files)

    return selected_files


def get_obs6_data(
        task,
        work_dir,
        config
) -> typing.List:
    input_dir = "Tier{tier}/{dataset}"
    input_file = "{project}_{dataset}_{type}_{version}_{mip}_{short_name}[_.]*nc"

    dataset = task["dataset"]
    project = dataset["project"]

    directories = [pathlib.Path(d, input_dir.format(**dataset)) for d in task["data_path"][project]]
    variables = task["variables"]

    selected_files = []
    for v in variables:
        combined_variable = {
            **dataset,
            **v,
        }
        filenames = [
            input_file.format(**combined_variable)
        ]

        files = find_files(
            directories,
            filenames
        )

        logger.info(f"Found files: {len(files)}")

        current_selected_files = select_files(
            files,
            start_year=combined_variable["start_year"],
            end_year=combined_variable["end_year"]
        )
        selected_files.extend(current_selected_files)

    return selected_files


def get_native6_data(
        task,
        work_dir,
        config
) -> typing.List:
    input_dir = "Tier{tier}/{dataset}/{version}/{frequency}/{short_name}"
    input_file = "*.nc"

    dataset = task["dataset"]
    project = dataset["project"]

    variables = task["variables"]

    selected_files = []
    for v in variables:
        combined_variable = {
            **dataset,
            **v
        }
        directories = [pathlib.Path(d, input_dir.format(**combined_variable)) for d in task["data_path"][project]]
        filenames = input_file.format(**combined_variable)

        current_files = find_files(
            directories,
            filenames
        )

        logger.info(f"Found files: {len(current_files)}")

        current_selected_files = select_files(
            current_files,
            start_year=dataset["start_year"],
            end_year=dataset["end_year"]
        )
        selected_files.extend(current_selected_files)

    return selected_files
