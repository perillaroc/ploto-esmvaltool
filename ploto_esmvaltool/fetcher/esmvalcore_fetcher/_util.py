import pathlib
import typing
import itertools

from esmvalcore._data_finder import find_files, select_files

from loguru import logger


def get_exp_data(
        variable: typing.Dict,
        config: typing.Dict,
) -> typing.List:
    project = variable["project"]

    exp = variable["exp"]
    if isinstance(exp, str):
        exp = [exp]

    ensemble = variable["ensemble"]
    if isinstance(ensemble, str):
        ensemble = [ensemble]

    directories = config["data_path"][project]

    selected_files = []

    iter = itertools.product(exp, ensemble)
    for e, ens in iter:
        combined_variable = {
            **variable,
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
        variable,
        config
) -> typing.List:
    input_dir = "Tier{tier}/{dataset}"
    input_file = "{project}_{dataset}_{type}_{version}_{mip}_{short_name}[_.]*nc"

    project = variable["project"]

    directories = [pathlib.Path(d, input_dir.format(**variable)) for d in config["data_path"][project]]

    selected_files = []

    logger.info(f"checking for variable {variable}")
    filenames = [
        input_file.format(**variable)
    ]

    files = find_files(
        directories,
        filenames
    )

    logger.info(f"Found files: {len(files)}")

    current_selected_files = select_files(
        files,
        start_year=variable["start_year"],
        end_year=variable["end_year"]
    )
    selected_files.extend(current_selected_files)

    return selected_files


def get_native6_data(
        variable,
        config
) -> typing.List:
    input_dir = "Tier{tier}/{dataset}/{version}/{frequency}/{short_name}"
    input_file = "*.nc"

    project = variable["project"]

    selected_files = []

    directories = [pathlib.Path(d, input_dir.format(**variable)) for d in config["data_path"][project]]
    filenames = [input_file.format(**variable)]

    current_files = find_files(
        directories,
        filenames
    )

    logger.info(f"Found files: {len(current_files)}")

    current_selected_files = select_files(
        current_files,
        start_year=variable["start_year"],
        end_year=variable["end_year"]
    )
    selected_files.extend(current_selected_files)

    return selected_files


def get_obs4mips_data(
        variable,
        config
) -> typing.List:
    input_dir = "Tier{tier}/{dataset}"
    input_file = "{short_name}_{dataset}_{level}_{version}_*.nc"

    project = variable["project"]

    selected_files = []

    directories = [pathlib.Path(d, input_dir.format(**variable)) for d in config["data_path"][project]]
    filenames = [input_file.format(**variable)]

    current_files = find_files(
        directories,
        filenames
    )

    logger.info(f"Found files: {len(current_files)}")

    current_selected_files = select_files(
        current_files,
        start_year=variable["start_year"],
        end_year=variable["end_year"]
    )
    selected_files.extend(current_selected_files)

    return selected_files
