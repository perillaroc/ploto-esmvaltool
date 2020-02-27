import os
import subprocess

from loguru import logger


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
            "settings_file_path": "some/path/to/settings.yml",
            "force": "false",
            "ignore_existing": "false",
            "log_level": "debug",
            "diag_script": {
                "group": "base",
                "name": "examples/diagnostic.py",
            }
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
        task["settings_file_path"],
    ]

    logger.info(f"command: {cmd}")
    result = subprocess.run(
        cmd,
        env=envs,
        # start_new_session=True,
        # shell=True,
    )

    logger.info('running esmvaltool_python_plotter...done')
