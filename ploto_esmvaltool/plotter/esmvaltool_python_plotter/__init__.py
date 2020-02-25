import os
from pathlib import Path
import subprocess
import json

from loguru import logger


def run_plotter(task: dict, work_dir: str, config: dict):
    """
    run esmvaltool python plotter

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
            "log_level": "debug"
        }
    work_dir: str

    config: dict
        {
        }

    """
    logger.info('running esmvaltool_python_plotter...')

    envs = os.environ.copy()
    envs["MPLBACKEND"] = "Agg"

    logger.info("run esmvaltool_python_plotter program...")

    cmd = [
        "/home/hujk/.pyenv/versions/anaconda3-2019.10/envs/esmvaltool/bin/python3",
        "/home/hujk/ploto/esmvaltool/study/esmvaltool/ESMValTool/esmvaltool/diag_scripts/examples/diagnostic.py",
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
