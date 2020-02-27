from copy import deepcopy
import os
import datetime

from loguru import logger

from esmvalcore._config import (
    configure_logging,
    CFG_USER,
    CFG,
    read_config_developer_file,
    read_cmor_tables,
    _normalize_path,
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
    _ = configure_logging(console_log_level="INFO")

    # get from recipe.yml
    recipe_documentation = task["recipe_documentation"]

    doc = deepcopy(recipe_documentation)
    for key in doc:
        if key in TAGS:
            doc[key] = replace_tags(key, doc[key])

    entity = get_recipe_provenance(doc, "recipe.yml")

    # get from _config.read_config_user_file function
    config_user = get_config_user(task["config"], task["recipe_name"])

    config_user['skip-nonexistent'] = False
    config_user['diagnostics'] = {}
    config_user['synda_download'] = False

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


def get_config_user(cfg: dict, recipe_name: str):
    # set defaults
    defaults = {
        'write_plots': True,
        'write_netcdf': True,
        'compress_netcdf': False,
        'exit_on_warning': False,
        'max_data_filesize': 100,
        'output_file_type': 'ps',
        'output_dir': './output_dir',
        'auxiliary_data_dir': './auxiliary_data',
        'save_intermediary_cubes': False,
        'remove_preproc_dir': False,
        'max_parallel_tasks': 1,
        'run_diagnostic': True,
        'profile_diagnostic': False,
        'config_developer_file': None,
        'drs': {},
    }

    for key in defaults:
        if key not in cfg:
            logger.info(
                "No %s specification in config file, "
                "defaulting to %s", key, defaults[key])
            cfg[key] = defaults[key]

    cfg['output_dir'] = _normalize_path(cfg['output_dir'])
    cfg['auxiliary_data_dir'] = _normalize_path(cfg['auxiliary_data_dir'])

    cfg['config_developer_file'] = _normalize_path(
        cfg['config_developer_file'])

    for key in cfg['rootpath']:
        root = cfg['rootpath'][key]
        if isinstance(root, str):
            cfg['rootpath'][key] = [_normalize_path(root)]
        else:
            cfg['rootpath'][key] = [_normalize_path(path) for path in root]

    # insert a directory date_time_recipe_usertag in the output paths
    now = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    new_subdir = '_'.join((recipe_name, now))
    cfg['output_dir'] = os.path.join(cfg['output_dir'], new_subdir)

    # create subdirectories
    cfg['preproc_dir'] = os.path.join(cfg['output_dir'], 'preproc')
    cfg['work_dir'] = os.path.join(cfg['output_dir'], 'work')
    cfg['plot_dir'] = os.path.join(cfg['output_dir'], 'plots')
    cfg['run_dir'] = os.path.join(cfg['output_dir'], 'run')

    # Save user configuration in global variable
    for key, value in cfg.items():
        CFG_USER[key] = value

    # Read developer configuration file
    cfg_developer = read_config_developer_file(cfg['config_developer_file'])
    for key, value in cfg_developer.items():
        CFG[key] = value
    read_cmor_tables(CFG)

    return cfg
