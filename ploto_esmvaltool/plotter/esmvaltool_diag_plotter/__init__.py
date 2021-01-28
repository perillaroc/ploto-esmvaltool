import os
import subprocess
import typing
from pathlib import Path

from loguru import logger
import yaml

from .util import add_input_files, replace_settings_directories


def run_plotter(
        task: typing.Dict,
        work_dir: str,
        config: typing.Dict
):
    """
    run esmvaltool python diagnostics script.

    Parameters
    ----------
    task: dict

    work_dir: str

    config: dict
        {
            "esmvaltool": {
                "executables": {
                    "py": "/some/path/to/python3"
                },
                "recipes": {
                    "base": "/some/path/to/ESMValTool/esmvaltool/recipes",
                },
                "diag_scripts": {
                    "base": "/some/path/to/ESMValTool/esmvaltool/diag_scripts",
                },
            }
        }

    """
    logger.info('running esmvaltool_diag_plotter...')

    envs = os.environ.copy()
    envs["MPLBACKEND"] = "Agg"

    logger.info("run esmvaltool_diag_plotter program...")

    input_files = task["input_files"]
    task_config = task["config"]
    task_diag = task["diag"]

    settings = {
        **task_diag,
        "input_files": input_files,
        **task_config,
    }

    settings = add_input_files(
        settings,
        input_files,
        work_dir
    )
    settings = replace_settings_directories(
        settings,
        work_dir
    )

    settings_file_path = Path(work_dir, "settings.yml")
    with open(settings_file_path, "w") as f:
        yaml.safe_dump(settings, f)

    diag_script_config = task["diag_script"]
    diag_script_path = Path(
        f"{config['esmvaltool']['diag_scripts'][diag_script_config['group']]}",
        f"{diag_script_config['name']}"
    )

    suffix = diag_script_path.suffix.lower()[1:]
    if suffix == "py":
        run_python_script(
            diag_script_path=diag_script_path,
            settings_file_path=settings_file_path,
            config=config
        )
    else:
        logger.error(f"script suffix is not supported: {suffix}")

    logger.info('running esmvaltool_python_plotter...done')


def run_python_script(
        diag_script_path,
        settings_file_path,
        config,
):
    executable = config["esmvaltool"]["executables"]["py"]

    cmd = [
        executable,
        diag_script_path,
        "-f",
        "-i",
        str(settings_file_path.absolute()),
    ]

    envs = os.environ.copy()
    envs["MPLBACKEND"] = "Agg"

    logger.info(f"python command: {cmd}")
    result = subprocess.run(
        cmd,
        env=envs,
        # start_new_session=True,
        # shell=True,
    )

    return result
