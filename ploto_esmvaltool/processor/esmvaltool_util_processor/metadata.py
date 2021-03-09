from pathlib import Path
import typing

import yaml

from ploto.logger import get_logger
from ploto_esmvaltool.processor.esmvalcore_pre_processor._product import update_product_output


logger = get_logger()


def combine_metadata(
        task: typing.Dict,
        work_dir: str,
        config: typing.Dict,
):
    """

    Parameters
    ----------
    task
        {
            "products": [
                {
                    "input": {
                        "input_metadata_files": [
                            # ...
                        ]
                    },
                    "output": {
                        "output_directory": ""
                    }
                }
            ],
            "output": {
                "output_directory": "..."
            }
        }
    work_dir
    config

    Returns
    -------

    """
    logger.info("running combine_metadata...")

    task_products = task["products"]
    task_output = task["output"]

    for product in task_products:
        product["output"] = update_product_output(product["output"], task_output)

        input_metadata_files = product["input"]["input_metadata_files"]
        data = dict()
        for mf in input_metadata_files:
            mf_path = mf.format(work_dir=work_dir)
            with open(mf_path) as f:
                metadata = yaml.safe_load(f)
                data = {**data, **metadata}

        output_file_name = "metadata.yml"
        output_file_path = Path(
            product["output"]["output_directory"].format(work_dir=work_dir),
            output_file_name
        )
        output_file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file_path, "w") as f:
            yaml.safe_dump(data, f, sort_keys=False)
        logger.info(f"write metadata to {str(output_file_path.absolute())}")

    logger.info("running combine_metadata...done")
