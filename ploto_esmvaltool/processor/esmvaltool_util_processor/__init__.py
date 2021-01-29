import typing
from pathlib import Path

from loguru import logger
import yaml


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
    logger.info("running combine_metadata...")
    output_directory = task["output_directory"].format(work_dir=work_dir)
    output_file_name = "metadata.yml"
    output_file_path = Path(output_directory, output_file_name)
    output_file_path.parent.mkdir(parents=True, exist_ok=True)

    data = dict()
    for mf in task["metadata_files"]:
        mf_path = mf.format(work_dir=work_dir)
        with open(mf_path) as f:
            metadata = yaml.safe_load(f)
            data = {**data, **metadata}

    with open(output_file_path, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False)
    logger.info(f"write metadata to {str(output_file_path.absolute())}")
    logger.info("running combine_metadata...done")
