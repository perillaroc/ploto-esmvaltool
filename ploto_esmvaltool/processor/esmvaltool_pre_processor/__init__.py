from copy import deepcopy
from pathlib import Path

from loguru import logger
import yaml

from esmvalcore._config import (
    configure_logging,
    read_config_user_file,
)
from esmvalcore._recipe import (
    get_recipe_provenance,
    TAGS,
    replace_tags,
    _get_preprocessor_task,
)


def run_processor(
        task: dict,
        work_dir: str,
        config: dict,
):
    """

    Parameters
    ----------
    task: dict
        {
            "task_name": "diagnostics/ta",
            "variables": [],
            "profiles": {},
            "config": {},
            "recipe_name": "recipe.yml",
            "recipe_documentation": {},
        }

    work_dir: str

    config: dict

    """
    logger.info("running processor: esmvaltool_pre_processor")
    _ = configure_logging(console_log_level="DEBUG")

    preprocessor_task = get_preprocessor_task(task, work_dir, config)

    output_files = preprocessor_task.run()
    logger.info(f"output files: {output_files}")

    logger.info("running processor done: esmvaltool_pre_processor")


def get_preprocessor_task(task: dict, work_dir: str, config: dict):
    config_user = get_config_user(task, work_dir)

    profiles = task["profiles"]
    variables = task["variables"]

    preprocessor_task = _get_preprocessor_task(
        variables=variables,
        profiles=profiles,
        config_user=config_user,
        task_name=task["task_name"],
    )

    # get from recipe.yml
    recipe_documentation = task["recipe_documentation"]
    entity = get_provenance(recipe_documentation, "recipe.yml")
    preprocessor_task.initialize_provenance(entity)
    return preprocessor_task


def get_config_user(task: dict, work_dir: str) -> dict:
    config_file_path = Path(work_dir, "config.yaml")
    with open(config_file_path, "w") as f:
        yaml.safe_dump(task["config"], f)
    config_user = read_config_user_file(config_file_path, task["recipe_name"])
    config_user = replace_config_directories(config_user, work_dir)

    config_user['skip-nonexistent'] = False
    config_user['diagnostics'] = {}
    config_user['synda_download'] = False

    return config_user


def replace_config_directories(config_user: dict, work_dir: str) -> dict:
    # modify run directories generate by config_user.
    config_user['output_dir'] = work_dir
    config_user['preproc_dir'] = str(Path(work_dir, 'preproc'))
    config_user['work_dir'] = str(Path(work_dir, 'work'))
    config_user['plot_dir'] = str(Path(work_dir, 'plots'))
    config_user['run_dir'] = str(Path(work_dir, 'run'))
    return config_user


def get_provenance(recipe_documentation: dict, file_name: str):
    doc = deepcopy(recipe_documentation)
    for key in doc:
        if key in TAGS:
            doc[key] = replace_tags(key, doc[key])

    entity = get_recipe_provenance(doc, file_name)
    return entity
