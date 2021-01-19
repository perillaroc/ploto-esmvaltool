import typing
from pathlib import Path

from loguru import logger
import yaml


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


    logger.info("running processor done: esmvalcore_pre_processor")