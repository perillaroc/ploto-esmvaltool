import os
import typing
from pathlib import Path

from loguru import logger
import yaml

from .run import (
    run_python_script,
    run_r_script
)
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
    task_diagnostic = task["diagnostic"]
    task_diagnostic_script = task["diagnostic_script"]

    settings = {
        **task_diagnostic,
        "input_files": input_files,
        **task_diagnostic_script["settings"],
        **task_config,
    }

    settings = add_input_files(
        settings,
        input_files,
        work_dir
    )

    step_work_dir = task.get("step_work_dir", work_dir).format(work_dir=work_dir)
    settings = replace_settings_directories(
        settings,
        step_work_dir,
    )

    run_dir = settings["run_dir"]

    settings_file_path = Path(
        run_dir,
        task_diagnostic["name"],
        task_diagnostic_script["settings"]["script"] ,
        "settings.yml"
    )

    settings_file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(settings_file_path, "w") as f:
        yaml.safe_dump(settings, f)

    diag_scripts = config['esmvaltool']['diag_scripts'][task_diagnostic_script["path"]['group']]
    diag_script_path = Path(
        diag_scripts,
        task_diagnostic_script["path"]['script']
    )

    suffix = diag_script_path.suffix.lower()[1:]
    if suffix == "py":
        run_python_script(
            diag_script_path=diag_script_path,
            settings_file_path=settings_file_path,
            config=config
        )
    elif suffix == "r":
        run_r_script(
            diag_script_path=diag_script_path,
            diag_scripts=diag_scripts,
            settings_file_path=settings_file_path,
            config=config,
        )
    else:
        logger.error(f"script suffix is not supported: {suffix}")

    logger.info('running esmvaltool_python_plotter...done')


