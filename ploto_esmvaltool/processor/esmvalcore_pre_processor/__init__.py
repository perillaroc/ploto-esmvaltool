import typing
from pathlib import Path

from loguru import logger

import ploto_esmvaltool.processor.esmvalcore_pre_processor.operations as esmvalcore_operations
from .operations import (
    run_load,
    run_save,
    run_write_metadata,
)


def run_processor(
        task: typing.Dict,
        work_dir: typing.Union[str, Path],
        config: typing.Dict,
):
    """

    Parameters
    ----------
    task: dict
        {
            "products": [
                {
                    "variable": {

                    }
                    "input": {
                        "input_data_source_file": ...
                        # or
                        "input_metadata_files": [

                        ]
                    },
                    "output": {
                        "output_file": "",
                    }
                }
            ],
            "generated_products": {
                "multi_model_statistic.mean": {
                    "output": {
                        "output_file": "",
                    }
                }
            },

            "output": {
                "output_directory": ""
            },

            "operations" : [
                {
                    "type": "operation_type",
                    "settings": {
                        "key": "value"
                    }
                }
            ],

            "diagnostic": {
                "diagnostic": "name"
            }
        }


    work_dir: str

    config: dict

    """
    logger.info("running processor: esmvalcore_pre_processor")

    operations = task["operations"]

    cube = None

    # load cube
    cube = run_load(
        operation={
            "type": "load"
        },
        task=task,
        cube=cube,
        work_dir=work_dir,
    )

    # run steps
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
    file_path = run_save(
        operation={},
        task=task,
        cubes=[cube],
        work_dir=work_dir,
    )
    logger.info(f"write file to {file_path}")

    output_metadata_file_name = task.get("output_metadata_file_name", "metadata.yml")

    # write metadata
    metadata = run_write_metadata(
        operation={},
        task=task,
        work_dir=work_dir,
        file_path=file_path,
        metadata_file_name=output_metadata_file_name,
    )
    logger.info(f"write metadata to {metadata.absolute()}")

    logger.info("running processor done: esmvalcore_pre_processor")
