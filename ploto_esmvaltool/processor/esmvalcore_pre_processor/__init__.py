import typing
from pathlib import Path

from loguru import logger
import yaml

import ploto_esmvaltool.processor.esmvalcore_pre_processor.operations as esmvalcore_operations

def run_processor(
        task: typing.Dict,
        work_dir: str,
        config: typing.Dict,
):
    """

    Parameters
    ----------
    task: dict

    work_dir: str

    config: dict

    """
    logger.info("running processor: esmvalcore_pre_processor")

    operations = task["operations"]

    cube = None
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
    file_path = esmvalcore_operations.run_save(
        operation={},
        task=task,
        cubes=[cube],
        work_dir=work_dir,
    )
    logger.info(f"write file to {file_path}")

    logger.info("running processor done: esmvalcore_pre_processor")