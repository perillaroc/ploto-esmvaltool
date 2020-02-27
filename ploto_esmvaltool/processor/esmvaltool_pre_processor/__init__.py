from copy import deepcopy
from loguru import logger

from esmvalcore._config import (
    configure_logging,
    CFG_USER,
    CFG,
    read_config_developer_file,
    read_cmor_tables,
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
            "config_user": {},
            "recipe_name": "recipe.yml",
            "recipe_documentation": {},
        }

    work_dir: str

    config: dict

    """
    logger.info("running processor: esmvaltool_pre_processor")
    _ = configure_logging(console_log_level="INFO")

    # get from recipe.yml
    recipe_documentation = task["recipe_documentation"]

    doc = deepcopy(recipe_documentation)
    for key in doc:
        if key in TAGS:
            doc[key] = replace_tags(key, doc[key])

    entity = get_recipe_provenance(doc, "recipe.yml")

    # get from _config.read_config_user_file function
    config_user = task["config_user"]

    # Save user configuration in global variable
    for key, value in config_user.items():
        CFG_USER[key] = value

    # Read developer configuration file
    cfg_developer = read_config_developer_file(config_user['config_developer_file'])
    for key, value in cfg_developer.items():
        CFG[key] = value
    read_cmor_tables(CFG)

    profiles = task["profiles"]

    variables = task["variables"]

    task = _get_preprocessor_task(
        variables=variables,
        profiles=profiles,
        config_user=config_user,
        task_name=task["task_name"],
    )
    task.initialize_provenance(entity)

    output_files = task.run()

    logger.info(f"output files: {output_files}")
    logger.info("running processor done: esmvaltool_pre_processor")
