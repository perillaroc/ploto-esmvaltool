import itertools
from pathlib import Path
import copy

from loguru import logger

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.util import (
    get_default_settings,
    is_multi_model_operation
)
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.bock20 import generate_default_operation_blocks
from ploto_esmvaltool.util.esmvaltool import (
    combine_variable,
    add_variable_info
)

from ploto_esmvaltool.fetcher.esmvalcore_fetcher import get_selected_files

from esmvalcore._recipe import (
    _special_name_to_dataset,
    _get_dataset_info,
    _exclude_dataset
)
from esmvalcore.preprocessor import MULTI_MODEL_FUNCTIONS

from test.recipes.atmos.bock20 import (
    config as bock20_config,
    recipe as bock20_recipe,
)


diagnostic_name = "fig_1_cmip6"


def _get_input_section(block_index, variable):
    if block_index == 0:
        return {
            "input_data_source_file":
                "{work_dir}"
                f"/{diagnostic_name}/fetcher/preproc/{variable['alias']}"
                f"/{variable['variable_group']}/data_source.yml",
        }
    else:
        return {
            "input_metadata_files": [
                "{work_dir}"
                f"/{diagnostic_name}/processor/preproc/step-{block_index-1:02}/{variable['alias']}"
                f"/{variable['variable_group']}/metadata.yml"
            ]
        }


def _get_output_section(block_index, variable):
    return {
        "output_directory": f"step-{block_index:02}" + "/{alias}/{variable_group}",
    }

def get_processor_tasks(
        variable,
        operation_block,
        block_index,
        settings,
):
    processor_tasks = []

    diag = {
        "diagnostic": diagnostic_name,
    }

    combined_variable = variable

    task = {
        "products": [
            {
                "variable": combined_variable,
                "input": _get_input_section(block_index, combined_variable),
                "output": _get_output_section(block_index, combine_variable),
                "settings": settings,
            }
        ],

        # output
        "output": {
            "output_directory": "{work_dir}" + f"/{diagnostic_name}/processor/preproc"
        },

        # operations
        "operations": operation_block,

        "diagnostic": diag,
    }
    processor_tasks.append(task)

    return processor_tasks


def get_multi_model_processor_tasks(
        variable_products,
        operation_block,
        block_index,
        # settings
):
    processor_tasks = []

    diag = {
        "diagnostic": diagnostic_name,
    }

    for op in operation_block:
        if op["type"] == "multi_model_statistics":
            op["settings"]["output"] = {
                "output_directory": f"step-{block_index:02}" + "/multi-model-{operator}/{variable_group}",
                "output_file": "MultiModel_{operator}_{mip}_{variable_group}_{start_year}-{end_year}.nc",
            }

    def get_product(variable, settings):
        return {
            "variable": variable,
            "input": _get_input_section(block_index, variable),
            "output": _get_output_section(block_index, variable),
            "settings": settings
        }

    task = {
        "products": [
            get_product(**variable) for variable in variable_products
        ],

        # output
        "output": {
            "output_directory": "{work_dir}" + f"/{diagnostic_name}/processor/preproc"
        },

        # operations
        "operations": operation_block,

        "diagnostic": diag,
    }
    processor_tasks.append(task)

    return processor_tasks


def get_tasks_for_variable(
        variable,
        datasets,
        additional_datasets,
        work_dir,
):
    """
    recipe_dataset_index 仅在单个变量组内计数，各个变量组之间独立
    """
    exp_datasets = [{
        **d,
        "recipe_dataset_index": index
    } for index, d in enumerate(datasets)]
    current_index = len(exp_datasets)

    additional_datasets = [{
        **d,
        "alias": f"{d['dataset']}-{d['project']}",
        "recipe_dataset_index": current_index + index
    } for index, d in enumerate(additional_datasets)]

    # 试验数据集
    def generate_exp_variable(
            variable,
            dataset,
    ):
        v = combine_variable(
            variable=variable,
            dataset=dataset
        )
        add_variable_info(v)
        v["alias"] = f"{v['dataset']}-{v['exp']}"
        return v

    exp_variables = [
        generate_exp_variable(variable=variable, dataset=d)
        for d in exp_datasets
    ]

    # 附加数据集
    def generate_reference_variable(
            variable,
            dataset,
    ):
        v = combine_variable(
            variable=variable,
            dataset=dataset
        )
        add_variable_info(v)
        v["alias"] = f"{v['dataset']}-{v['project']}"
        return v

    additional_variables = [
        generate_reference_variable(
            variable=variable,
            dataset=d
        )
        for d in additional_datasets
    ]

    # 合并两个数据集
    variables = [
        *exp_variables,
        *additional_variables,
    ]

    processor_tasks = []

    # 获取预处理器参数
    settings = bock20_recipe.processor_settings[variable["preprocessor"]]
    settings = {
        **get_default_settings(),
        **settings,
    }

    # 获取预处理块
    blocks = generate_default_operation_blocks(
        variable["preprocessor"],
        settings,
    )

    # 生成 processor 任务
    for block_index, operation_block in enumerate(blocks):
        # 处理预处理器参数
        variable_products = []
        for v in variables:
            variable_settings = copy.deepcopy(settings)
            # 更新 target_grid
            update_target_grid(
                v,
                variables,
                variable_settings,
                config={
                    "data_path": bock20_config.data_path
                }
            )

            # 更新多模式步骤
            update_multi_dataset_settings(v, variable_settings)

            variable_products.append({
                "variable": v,
                "settings": variable_settings
            })

        # 生成 processor 任务
        if is_multi_model_operation(operation_block[0]):
            processor_tasks.extend(get_multi_model_processor_tasks(
                variable_products,
                operation_block=operation_block,
                block_index=block_index,
                # settings=settings
            ))
        else:
            for p in variable_products:
                processor_tasks.extend(get_processor_tasks(
                    variable=p["variable"],
                    operation_block=operation_block,
                    block_index=block_index,
                    settings=p["settings"]
                ))

    return processor_tasks


def update_target_grid(
        variable,
        variables,
        settings,
        config,
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
        variable,
        settings,
):
    for step in MULTI_MODEL_FUNCTIONS:
        if not settings.get(step):
            continue
        exclude_dataset(settings, variable, step)


def exclude_dataset(settings, variable, step):
    exclude = {
        _special_name_to_dataset(variable, dataset)
        for dataset in settings[step].pop('exclude', [])
    }
    if variable['dataset'] in exclude:
        # 排除的数据集将该步骤参数设为 None
        settings[step] = None
        logger.info(f"Excluded dataset '{variable['dataset']}' from preprocessor step '{step}'")


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case108/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    processor_tasks = []

    # add recipe_dataset_index
    exp_datasets = bock20_recipe.exp_datasets
    variables = bock20_recipe.variables

    # 观测数据
    variable_additional_datasets = bock20_recipe.variable_additional_datasets
    for variable in variables:
        if variable["variable_group"] in variable_additional_datasets:
            additional_datasets = variable_additional_datasets[variable["variable_group"]]
        else:
            additional_datasets = []
        processor_tasks.extend(
            get_tasks_for_variable(
                variable=variable,
                datasets=exp_datasets,
                additional_datasets=additional_datasets,
                work_dir=work_dir
            )
        )

    for task in processor_tasks:
        run_processor(
            task,
            config={},
            work_dir=work_dir
        )


if __name__ == "__main__":
    main()
