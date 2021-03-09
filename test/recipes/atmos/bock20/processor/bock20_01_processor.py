import itertools
from pathlib import Path
import copy

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.util import (
    get_default_settings,
    is_multi_model_operation
)
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.bock20 import generate_default_operation_blocks
from ploto_esmvaltool.util.esmvaltool import (
    get_datasets,
    update_variable_settings
)
from ploto_esmvaltool.util.task import (
    get_product_processor_tasks,
    get_multi_model_processor_tasks,
)

from test.recipes.atmos.bock20 import (
    config as bock20_config,
    recipe as bock20_recipe,
)


diagnostic_name = "fig_1_cmip6"


def get_tasks_for_variable(
        variable,
        datasets,
        work_dir,
):
    variables = datasets
    diagnostic = {
        "diagnostic": diagnostic_name
    }

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
            variable_settings = update_variable_settings(
                variable=v,
                settings=variable_settings,
                variables=variables,
                config={
                    "data_path": bock20_config.data_path
                }
            )

            variable_products.append({
                "variable": v,
                "settings": variable_settings
            })

        # 生成 processor 任务
        if is_multi_model_operation(operation_block[0]):
            processor_tasks.extend(get_multi_model_processor_tasks(
                diagnostic=diagnostic,
                variable_products=variable_products,
                operation_block=operation_block,
                block_index=block_index,
            ))
        else:
            for p in variable_products:
                processor_tasks.extend(get_product_processor_tasks(
                    diagnostic=diagnostic,
                    variable_product=p,
                    operation_block=operation_block,
                    block_index=block_index,
                ))

    return processor_tasks


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case108/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    # recipe
    exp_datasets = bock20_recipe.exp_datasets
    variables = bock20_recipe.variables
    variable_additional_datasets = bock20_recipe.variable_additional_datasets

    # get all datasets
    datasets = get_datasets(
        datasets=exp_datasets,
        variables=variables,
        variable_additional_datasets=variable_additional_datasets
    )

    processor_tasks = []
    for variable in variables:
        processor_tasks.extend(
            get_tasks_for_variable(
                variable=variable,
                datasets=datasets[variable["variable_group"]],
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
