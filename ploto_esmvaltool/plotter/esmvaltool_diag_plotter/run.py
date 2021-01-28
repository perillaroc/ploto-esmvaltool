import os
import subprocess

from loguru import logger


def get_python_cmd(
        diag_script_path,
        config
):
    executable = config["esmvaltool"]["executables"]["py"]

    cmd = [
        executable,
        diag_script_path,
    ]

    return cmd


def get_python_env():
    envs = os.environ.copy()
    envs["MPLBACKEND"] = "Agg"
    return envs


def run_python_script(
        diag_script_path,
        settings_file_path,
        config,
):

    cmd = get_python_cmd(diag_script_path, config)
    cmd.extend([
        "-f",
        "-i",
        str(settings_file_path.absolute()),
    ])

    envs = get_python_env()

    logger.info(f"python command: {cmd}")
    result = subprocess.run(
        cmd,
        env=envs,
        # start_new_session=True,
        # shell=True,
    )

    return result


def get_r_cmd(
        diag_script_path,
        config
):
    executable = config["esmvaltool"]["executables"]["r"]

    cmd = [
        executable,
        diag_script_path,
    ]

    return cmd


def get_r_env(diag_scripts):
    envs = os.environ.copy()
    envs["diag_scripts"] = diag_scripts
    return envs


def run_r_script(
        diag_script_path,
        settings_file_path,
        diag_scripts,
        config,
):

    cmd = get_r_cmd(diag_script_path, config)
    cmd.extend([
        str(settings_file_path.absolute()),
    ])

    envs = get_r_env(diag_scripts)

    logger.info(f"python command: {cmd}")
    result = subprocess.run(
        cmd,
        env=envs,
        # start_new_session=True,
        # shell=True,
    )

    return result
