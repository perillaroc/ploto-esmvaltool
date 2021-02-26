import typing
from pathlib import Path

from ploto.logger import get_logger

import ploto_esmvaltool.processor.esmvalcore_pre_processor.operations as esmvalcore_operations
from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations import (
    run_load,
    run_save,
    run_write_metadata,
)

from ._product import (
    _add_diagnostic,
    _update_product_output
)

from .operations.util import is_multi_model_operation


logger = get_logger()


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
                    },

                    # operation settings
                    "settings": {
                        "extract_levels": {
                            #...
                        }
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

    task_products = task["products"]
    operations = task["operations"]
    task_output = task["output"]
    task_diagnostic = task["diagnostic"]

    if is_multi_model_operation(operations[0]):
        raise NotImplementedError("Multi Model Operations are not implemented")
    else:
        for product in task_products:
            product = _add_diagnostic(product, task_diagnostic)
            product = _update_product_output(product, task_output)
            run_operation_block(
                product=product,
                operations=operations,
                work_dir=work_dir
            )

    logger.info("running processor done: esmvalcore_pre_processor")


def run_multi_model_operation_block(
        products,
        operations,
        work_dir
):
    pass


def run_operation_block(
        product,
        operations,
        work_dir
):
    cube = None

    # load cube
    cube = run_load(
        operation={
            "type": "load"
        },
        product=product,
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
            product=product,
            cube=cube,
            work_dir=work_dir,
        )

    # save to workdir
    file_path = run_save(
        operation={},
        product=product,
        cubes=[cube],
        work_dir=work_dir,
    )
    logger.info(f"write file to {file_path}")

    output_metadata_file_name = product["output"].get(
        "output_metadata_file_name", "metadata.yml"
    )

    # write metadata
    metadata = run_write_metadata(
        operation={},
        product=product,
        work_dir=work_dir,
        file_path=file_path,
        metadata_file_name=output_metadata_file_name,
    )
    logger.info(f"write metadata to {metadata.absolute()}")
