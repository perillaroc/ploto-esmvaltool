import os
import typing
from pathlib import Path

from loguru import logger
import yaml

from .run import (
    run_python_script,
    run_r_script,
    run_ncl_script,
)
from .util import add_input_files, replace_settings_directories


from esmvalcore.preprocessor._io import write_ncl_settings


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

    input_files = task["input_files"]
    task_config = task["config"]
    task_diagnostic = task["diagnostic"]
    task_diagnostic_script = task["diagnostic_script"]
    step_work_dir = task.get("step_work_dir", work_dir).format(work_dir=work_dir)

    settings = {
        **task_diagnostic,
        "input_files": input_files,
        **task_diagnostic_script["settings"],
        **task_config,
    }

    diag_scripts = config['esmvaltool']['diag_scripts'][task_diagnostic_script["path"]['group']]
    diag_script_path = Path(
        diag_scripts,
        task_diagnostic_script["path"]['script']
    )

    # add input files
    suffix = diag_script_path.suffix.lower()[1:]
    if suffix == "ncl":
        settings = add_input_files(
            settings,
            input_files,
            work_dir,
            suffix=".ncl"
        )
    else:
        settings = add_input_files(
            settings,
            input_files,
            work_dir
        )

    # replace directories
    settings = replace_settings_directories(
        settings,
        step_work_dir,
    )

    # write settings
    run_dir = settings["run_dir"]
    settings_file_path = Path(
        run_dir,
        task_diagnostic["name"],
        task_diagnostic_script["settings"]["script"],
        "settings.yml"
    )
    settings_file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(settings_file_path, "w") as f:
        yaml.safe_dump(settings, f)

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
    elif suffix == "ncl":
        ncl_settings_path = write_ncl_script_settings(settings)
        logger.info(f"write ncl settings: {ncl_settings_path}")

        settings_file_path = ncl_settings_path
        run_ncl_script(
            diag_script_path=diag_script_path,
            diag_scripts=diag_scripts,
            settings_file_path=settings_file_path,
            config=config,
        )
    else:
        logger.error(f"script suffix is not supported: {suffix}")

    logger.info('running esmvaltool_python_plotter...done')


def write_ncl_script_settings(
        settings
):
    """
    Notes
    -----
    Copy from _write_ncl_settings() method from esmvalcore._task.DiagnosticTask class.
    """
    filename = Path(settings['run_dir']) / 'settings.ncl'

    config_user_keys = {
        'run_dir',
        'plot_dir',
        'work_dir',
        'output_file_type',
        'log_level',
    }

    ncl_settings = {
        'diag_script_info': {},
        'config_user_info': {}
    }

    for key, value in settings.items():
        if key in config_user_keys:
            ncl_settings['config_user_info'][key] = value
        elif not isinstance(value, dict):
            ncl_settings['diag_script_info'][key] = value
        else:
            ncl_settings[key] = value

    # Still add deprecated keys to config_user_info to avoid
    # crashing the diagnostic script that need this.
    # DEPRECATED: remove in v2.4
    for key in ('write_plots', 'write_netcdf'):
        if key in settings:
            ncl_settings['config_user_info'][key] = settings[key]

    write_ncl_settings(ncl_settings, filename)

    return filename
