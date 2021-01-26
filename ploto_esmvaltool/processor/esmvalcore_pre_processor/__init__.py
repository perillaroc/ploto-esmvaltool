import typing
from pathlib import Path

from loguru import logger

import ploto_esmvaltool.processor.esmvalcore_pre_processor.operations as esmvalcore_operations
import ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.io


def run_processor(
        task: typing.Dict,
        work_dir: typing.Union[str, Path],
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
    file_path = ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.io.run_save(
        operation={},
        task=task,
        cubes=[cube],
        work_dir=work_dir,
    )
    logger.info(f"write file to {file_path}")

    output_metadata_file_name = task.get("output_metadata_file_name", "metadata.yml")

    metadata = ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.io.run_write_metadata(
        operation={},
        task=task,
        work_dir=work_dir,
        file_path=file_path,
        metadata_file_name=output_metadata_file_name,
    )
    logger.info(f"write metadata to {metadata.absolute()}")

    logger.info("running processor done: esmvalcore_pre_processor")
