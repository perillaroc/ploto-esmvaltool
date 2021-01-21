import os
import subprocess
import typing
from pathlib import Path

from loguru import logger
import yaml


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
    diag_script_path = (
        f"{config['esmvaltool']['diag_scripts'][diag_script_config['group']]}/"
        f"{diag_script_config['name']}"
    )
    executable = config["esmvaltool"]["executables"]["py"]

    cmd = [
        executable,
        diag_script_path,
        "-f",
        "-i",
        str(settings_file_path.absolute()),
    ]

    logger.info(f"command: {cmd}")
    result = subprocess.run(
        cmd,
        env=envs,
        # start_new_session=True,
        # shell=True,
    )

    logger.info('running esmvaltool_python_plotter...done')


def add_input_files(
        settings: typing.Dict,
        input_files: typing.List,
        work_dir: str
) -> typing.Dict:
    """
    Add input files, only yaml files are supported.

    Parameters
    ----------
    settings: dict
        settings from plotter's task
    input_files: list
        input file list
    work_dir: str

    Returns
    -------
    dict:
        settings with input files
    """
    settings['input_files'] = [
        f.format(work_dir=work_dir) for f in input_files
        if f.endswith('.yml') or os.path.isdir(f)
    ]
    return settings


def replace_settings_directories(
        settings: typing.Dict,
        work_dir: str
) -> typing.Dict:
    """
    Replace directories using work dir.

    Parameters
    ----------
    settings: dict
        settings from plotter's task
    work_dir: str
        task work dir
    Returns
    -------
    dict:
        settings with work dir
    """
    settings['work_dir'] = str(Path(work_dir, 'work'))
    settings['plot_dir'] = str(Path(work_dir, 'plots'))
    settings['run_dir'] = str(Path(work_dir, 'run'))
    return settings
