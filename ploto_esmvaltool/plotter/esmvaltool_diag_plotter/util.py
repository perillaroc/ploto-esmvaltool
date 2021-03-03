import os
import typing
from pathlib import Path


def add_input_files(
        settings: typing.Dict,
        input_files: typing.List,
        work_dir: str,
        suffix: str = ".yml"
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
    suffix: str

    Returns
    -------
    dict:
        settings with input files
    """
    input_files = [f.format(work_dir=work_dir) for f in input_files]
    settings['input_files'] = [
        f for f in input_files
        if f.endswith(suffix) or os.path.isdir(f)
    ]
    return settings


def replace_settings_directories(
        settings: typing.Dict,
        step_work_dir: str
) -> typing.Dict:
    """
    Replace directories using work dir.

    Parameters
    ----------
    settings: dict
        settings from plotter's task
    step_work_dir: str
        task work dir
    Returns
    -------
    dict:
        settings with work dir
    """
    settings['work_dir'] = str(Path(step_work_dir, 'work'))
    settings['plot_dir'] = str(Path(step_work_dir, 'plots'))
    settings['run_dir'] = str(Path(step_work_dir, 'run'))
    return settings
