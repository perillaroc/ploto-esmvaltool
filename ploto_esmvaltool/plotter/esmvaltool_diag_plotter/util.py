import os
import typing
from pathlib import Path


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
