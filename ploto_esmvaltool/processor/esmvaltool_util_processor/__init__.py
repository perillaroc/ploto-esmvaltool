import typing
from pathlib import Path

from loguru import logger

from ploto_esmvaltool.processor.esmvaltool_util_processor.metadata import combine_metadata


util_mapper = {
    "combine_metadata": combine_metadata
}


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

    try:
        util_func = util_mapper[util_type]
    except KeyError:
        logger.error(f"util type is not supported: {util_type}")
        raise

    util_func(
            task,
            work_dir,
            config,
    )

    logger.info("running processor done: esmvaltool_util_processor")
