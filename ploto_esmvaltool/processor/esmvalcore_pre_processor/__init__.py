import typing
from pathlib import Path

from ploto.logger import get_logger

import ploto_esmvaltool.processor.esmvalcore_pre_processor.operations as esmvalcore_operations

from .operations.util import (
    _get_settings,
    is_multi_model_operation
)
from ._product import Product


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

    products = [Product(**task_product) for task_product in task_products]


    if is_multi_model_operation(operations[0]):
        for product in products:
            product.add_diagnostic(task_diagnostic)
            product.update_output(task_output)
        run_multi_model_operation_block(
            products=products,
            operation_block=operations,
            work_dir=work_dir
        )
    else:
        for product in products:
            product.add_diagnostic(task_diagnostic)
            product.update_output(task_output)
            product.run_operation_block(
                operation_block=operations,
                work_dir=work_dir
            )

    logger.info("running processor done: esmvalcore_pre_processor")


def run_operation_block(
        product: Product,
        operation_block: typing.Dict,
        work_dir: typing.Union[str, Path]
):
    if product.cubes is None:
        product.cubes = product.load(work_dir=work_dir)

    # run steps
    for step in operation_block:
        op = step["type"]
        logger.info(f"run step {op}")
        fun = getattr(esmvalcore_operations, f"run_{op}")
        settings = _get_settings(step, product.settings)
        product.cubes = fun(
            # operation=step,
            cube=product.cubes,
            variable=product.variable,
            settings=settings,
            work_dir=work_dir,
        )

    # save to workdir
    file_path = product.save(work_dir=work_dir)
    logger.info(f"write file to {file_path}")

    # write metadata
    metadata = product.write_metadata(file_path, work_dir=work_dir)
    logger.info(f"write metadata to {metadata.absolute()}")


def run_multi_model_operation_block(
        products: typing.List[Product],
        operation_block: typing.Dict,
        work_dir: typing.Union[str, Path]
):
    # load all product
    for product in products:
        if product.cubes is None:
            product.cubes = product.load(work_dir=work_dir)

    for step in operation_block:
        # multi model operation uses settings in operation.

        # check exclude

        # run operation step

        products = apply_multi_model_step(
            operation=step,
            products=products,
            work_dir=work_dir
        )

    for product in products:
        # save to workdir
        file_path = product.save(work_dir=work_dir)
        logger.info(f"write file to {file_path}")

        # write metadata
        metadata = product.write_metadata(file_path, work_dir=work_dir)
        logger.info(f"write metadata to {metadata.absolute()}")


def apply_multi_model_step(
        operation,
        products,
        work_dir,
):
    op = operation["type"]
    logger.info(f"run step {op}")
    fun = getattr(esmvalcore_operations, f"run_{op}")
    settings = operation["settings"]
    products = fun(
        products=products,
        **settings,
        work_dir=work_dir,
    )
    return products
