import itertools
import copy
from pathlib import Path

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.util import (
    get_default_settings,
    is_multi_model_operation
)
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.eyring13 import generate_default_operation_blocks
from ploto_esmvaltool.util.esmvaltool import (
    get_datasets,
    update_variable_settings,
)
from ploto_esmvaltool.util.task import (
    get_processor_tasks,
    get_multi_model_processor_tasks,
)

from test.recipes.atmos.eyring13 import (
    config as eyring13_config,
    recipe as eyring13_recipe,
)


def get_tasks_for_variable(
        variable,
        datasets,
        config,
        work_dir,
):
    variables = datasets

    processor_tasks = []

    # get operation blocks
    settings = eyring13_recipe.processor_settings[variable["preprocessor"]]
    settings = {
        **get_default_settings(),
        **settings,
    }


    blocks = generate_default_operation_blocks(
        variable["preprocessor"],
        settings,
    )

    # get processor tasks
    for block_index, operation_block in enumerate(blocks):
        variable_products = []
        for v in variables:
            variable_settings = copy.deepcopy(settings)
            variable_settings = update_variable_settings(
                variable=v,
                settings=variable_settings,
                variables=variables,
                config=config,
            )

            variable_products.append({
                "variable": v,
                "settings": variable_settings
            })


        if is_multi_model_operation(operation_block[0]):
            processor_tasks.extend(get_multi_model_processor_tasks(
                "fig12",
                variable_products=variable_products,
                operation_block=operation_block,
                block_index=block_index,
            ))
        else:
            for p in variable_products:
                processor_tasks.extend(get_processor_tasks(
                    "fig12",
                    variable_product=p,
                    operation_block=operation_block,
                    block_index=block_index,
                ))

    return processor_tasks


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case107/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    exp_datasets = eyring13_recipe.exp_datasets
    variables = eyring13_recipe.variables
    variable_additional_datasets = eyring13_recipe.variable_additional_datasets

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
                config={
                    "data_path": eyring13_config.data_path
                },
                work_dir=work_dir,
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
