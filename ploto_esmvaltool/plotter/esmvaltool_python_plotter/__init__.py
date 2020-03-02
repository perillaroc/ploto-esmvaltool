import os
import subprocess
from pathlib import Path

from loguru import logger
import yaml


def run_plotter(task: dict, work_dir: str, config: dict):
    """
    run esmvaltool python diagnostics script.

    Parameters
    ----------
    task:
        a dict config of plotter task.
        {
            "step_type": "plotter",
            "type": "ploto_esmvaltool.plotter.esmvaltool_python_plotter",
            "force": "false",
            "ignore_existing": "false",
            "log_level": "debug",
            "diag_script": {
                "group": "base",
                "name": "examples/diagnostic.py",
            },
            "settings": {
            },
            "input_files": [

            ]
        }
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
    logger.info('running esmvaltool_python_plotter...')

    envs = os.environ.copy()
    envs["MPLBACKEND"] = "Agg"

    logger.info("run esmvaltool_python_plotter program...")

    settings = task["settings"]
    input_files = task["input_files"]
    settings = add_input_files(settings, input_files)
    settings = replace_settings_directories(settings, work_dir)

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
        settings_file_path,
    ]

    logger.info(f"command: {cmd}")
    result = subprocess.run(
        cmd,
        env=envs,
        # start_new_session=True,
        # shell=True,
    )

    logger.info('running esmvaltool_python_plotter...done')


def add_input_files(settings: dict, input_files: list) -> dict:
    """
    Add input files, only yaml files are supported.

    Parameters
    ----------
    settings: dict
        settings from plotter's task
    input_files: list
        input file list

    Returns
    -------
    dict:
        settings with input files
    """
    settings['input_files'] = [
        f for f in input_files
        if f.endswith('.yml') or os.path.isdir(f)
    ]
    return settings


def replace_settings_directories(settings: dict, work_dir: str) -> dict:
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
