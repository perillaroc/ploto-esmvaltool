import typing
import copy
import os

from ploto_esmvaltool.fetcher.esmvalcore_fetcher import get_selected_files
from ploto.logger import get_logger


from esmvalcore._recipe import (
    _special_name_to_dataset,
    _get_dataset_info,
    get_reference_levels,
    get_cmor_levels
)
from esmvalcore.preprocessor import MULTI_MODEL_FUNCTIONS


logger = get_logger()


def update_variable_settings(
    variable: typing.Dict,
    settings: typing.Dict,
    variables: typing.List,
    config: typing.Dict,
):
    """
    Update operation block settings for variable (combined variable).

    Parameters
    ----------
    variable
    settings
    variables
    config

    Returns
    -------

    """
    # 更新 target_grid
    update_target_grid(
        variable,
        settings,
        variables,
        config=config
    )

    update_target_levels(
        variable,
        settings,
        variables,
        config=config
    )

    # 更新多模式步骤
    update_multi_dataset_settings(variable, settings)

    return settings


def update_target_grid(
        variable: typing.Dict,
        settings: typing.Dict,
        variables: typing.List,
        config: typing.Dict,
):
    """
    更新 regrid 步骤的 target_grid 配置项
    """
    grid = settings.get('regrid', {}).get('target_grid')
    if not grid:
        return

    grid = _special_name_to_dataset(variable, grid)

    if variable['dataset'] == grid:
        settings['regrid'] = None
    elif any(grid == v['dataset'] for v in variables):
        v = _get_dataset_info(grid, variables)
        selected_files = get_selected_files(
            v, config
        )
        settings['regrid']['target_grid'] = selected_files[0]
    return settings


def update_multi_dataset_settings(
        variable: typing.Dict,
        settings: typing.Dict,
):
    for step in MULTI_MODEL_FUNCTIONS:
        if not settings.get(step):
            continue
        exclude_dataset(settings, variable, step)


def exclude_dataset(settings: typing.Dict, variable: typing.Dict, step: str):
    """
    see esmvalcore._recipe._exclude_dataset function.

    Parameters
    ----------
    settings
    variable
    step

    Returns
    -------
    None
    """
    exclude = {
        _special_name_to_dataset(variable, dataset)
        for dataset in settings[step].pop('exclude', [])
    }
    if variable['dataset'] in exclude:
        # 排除的数据集将该步骤参数设为 None
        settings[step] = None
        logger.info(f"Excluded dataset '{variable['dataset']}' from preprocessor step '{step}'")


def update_target_levels(
        variable: typing.Dict,
        settings: typing.Dict,
        variables: typing.List,
        config: typing.Dict,
):
    levels = settings.get('extract_levels', {}).get('levels')
    if not levels:
        return

    levels = _special_name_to_dataset(variable, levels)

    if variable['dataset'] == levels:
        settings['extract_levels'] = None
    elif any(levels == v['dataset'] for v in variables):
        settings['extract_levels']['levels'] = {'dataset': levels}
        levels = settings['extract_levels']['levels']

    if not isinstance(levels, dict):
        return

    if 'cmor_table' in levels and 'coordinate' in levels:
        settings['extract_levels']['levels'] = get_cmor_levels(
            levels['cmor_table'], levels['coordinate'])
    elif 'dataset' in levels:
        dataset = levels['dataset']
        if variable['dataset'] == dataset:
            del settings['extract_levels']
        else:
            variable_data = _get_dataset_info(dataset, variables)
            filename = get_selected_files(variable_data, config)[0]
            settings['extract_levels']['levels'] = get_reference_levels(
                filename=filename,
                project=variable_data['project'],
                dataset=dataset,
                short_name=variable_data['short_name'],
                mip=variable_data['mip'],
                frequency=variable_data['frequency'],
                fix_dir=os.path.splitext(filename)[0] + '_fixed',
            )
