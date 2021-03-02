from pathlib import Path
import yaml


from ploto_esmvaltool.processor.esmvalcore_pre_processor._product import update_product_output
from ploto.logger import get_logger

from esmvalcore.preprocessor._io import _write_ncl_metadata

logger = get_logger()


def write_ncl_metadata(
        task,
        work_dir,
        config,
):
    """

    Parameters
    ----------
    task: typing.Dict
        {
            "products": [
                {
                    "input": {
                        "input_metadata_files": [

                        ]
                    },
                    "output": {
                        "output_directory": ""
                    }
                }
            ],
            "output": {
                "output_directory": ""
            },
        }
    work_dir
    config

    Returns
    -------

    """
    logger.info("running write_ncl_metadata...")

    task_products = task["products"]
    task_output = task["output"]

    for product in task_products:
        product["output"] = update_product_output(product["output"], task_output)

        metadata = {}

        input_metadata_files = product["input"]["input_metadata_files"]
        for metadata_path in input_metadata_files:
            metadata_path = metadata_path.format(work_dir=work_dir)
            with open(metadata_path, "r") as f:
                m = yaml.safe_load(f)
                metadata.update(m)

        ncl_metadata_path = _write_ncl_metadata(
            output_dir=product["output"]["output_directory"].format(work_dir=work_dir),
            metadata=metadata
        )
        logger.info(f"write ncl metadata to {ncl_metadata_path}")

    logger.info("running write_ncl_metadata...done")
