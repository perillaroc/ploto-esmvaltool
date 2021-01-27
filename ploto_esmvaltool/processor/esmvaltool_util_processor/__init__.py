import typing
from pathlib import Path

from loguru import logger


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
    logger.info("running processor: esmvaltool_util_processor")
    util_type = task["util_type"]
    if util_type == "combine_metadata":
        combine_metadata(
            task,
            work_dir,
            config,
        )
    else:
        logger.error(f"util type is not supported: {util_type}")

    logger.info("running processor done: esmvaltool_util_processor")


def combine_metadata(
        task,
        work_dir,
        config,
):
    pass
