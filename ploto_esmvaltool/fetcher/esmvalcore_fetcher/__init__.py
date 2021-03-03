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
    get_obs4mips_data,
    get_obs_data,
)

logger = get_logger()


def get_data(
        task: typing.Dict,
        work_dir: typing.Union[pathlib.Path, str],
        config: typing.Dict,
):
    """

    Parameters
    ----------
    task: typing.Dict
        {
            "products": [
                {
                    "variable": {
                        
                    },  # 通用 variable 结构
                    "output": {
                        "output_directory": "",  # optioinal
                        "output_data_source_file": "",
                    }
                }
            ],
            "output": {
                "output_directory": ""
            },
            "config": {
                "data_path": {
                    "CMIP6": [
                        "...",
                    ],
                    "OBS6": [
                        "...",
                    ],
                    "...": [
                        "..."
                    ]
                }
            }
        }
    work_dir: typing.Union[pathlib.Path, str]

    config: typing.Dict

    Returns
    -------

    """
    task_products = task["products"]
    task_config = task["config"]
    task_output = task["output"]
    for product in task_products:
        variable = product["variable"]
        product_output = product["output"].copy()

        output_directory = task_output.get("output_directory", "")
        product_output_directory = product_output.get("output_directory", "")
        output_directory = str(pathlib.Path(
            output_directory,
            product_output_directory
        ))

        product_output["output_directory"] = output_directory

        selected_files = get_selected_files(
            variable,
            task_config,
        )

        logger.info(f"Selected files: {len(selected_files)}")
        for f in selected_files:
            print(f)

        # write to metadata
        output_metadata_path = pathlib.Path(
            product_output["output_directory"].format(
                work_dir=work_dir,
                **variable,
            ),
            product_output["output_data_source_file"]
        )

        output_metadata_path.parent.mkdir(parents=True, exist_ok=True)

        data_source = {
            "input_files": [str(f) for f in selected_files]
        }

        with open(output_metadata_path, "w") as f:
            yaml.safe_dump(data_source, f)

        logger.info(f"write data source file: {str(output_metadata_path)}")


def get_selected_files(
        variable: typing.Dict,
        config: typing.Dict,
) -> typing.List:
    if "type" in variable:
        dataset_type = variable["type"]
    else:
        dataset_type = "exp"

    project = variable["project"]

    if dataset_type == "exp" and project == "CMIP6":
        selected_files = get_exp_data(
            variable=variable,
            config=config,
        )
    elif dataset_type == "reanaly" and project == "OBS6":
        selected_files = get_obs6_data(
            variable=variable,
            config=config,
        )
    elif dataset_type == "reanaly" and project == "native6":
        selected_files = get_native6_data(
            variable=variable,
            config=config,
        )
    elif project == "obs4mips":
        selected_files = get_obs4mips_data(
            variable=variable,
            config=config,
        )
    elif project == "OBS":
        selected_files = get_obs_data(
            variable=variable,
            config=config,
        )
    else:
        logger.exception(f"dataset type is not supported: {variable}")

    return selected_files
