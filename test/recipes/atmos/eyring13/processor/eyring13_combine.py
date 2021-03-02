import itertools
from pathlib import Path

from ploto_esmvaltool.processor.esmvaltool_util_processor import run_processor
from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.util import (
    get_default_settings,
    is_multi_model_operation
)
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.eyring13 import generate_default_operation_blocks
from ploto_esmvaltool.util.esmvaltool import (
    combine_variable,
    add_variable_info
)

from test.recipes.atmos.eyring13 import (
    config as eyring13_config,
    recipe as eyring13_recipe,
)
from test.recipes.atmos.eyring13.util import update_levels


diagnostic_name = "fig12"


def get_combine_task(
        variables,
        variable,
        block_index,
):
    task = {
        "util_type": "combine_metadata",
        "metadata_files": [
            "{work_dir}" + f"/{diagnostic_name}/processor/preproc/step-{block_index:02}/{d['alias']}/{d['variable_group']}/metadata.yml"
            for d in variables
        ],
        "output_directory": "{work_dir}" + f"/{diagnostic_name}/processor/preproc/{variable['variable_group']}",
    }

    return task


def get_tasks_for_variable(
        variable,
        datasets,
        additional_datasets,
        work_dir,
):
    """
    recipe_dataset_index 仅在单个变量组内计数，各个变量组之间独立
    """
    # get recipe dataset index
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

    # get exp variables
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

    # get additional variables
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

    tasks = [
        *exp_variables,
        *additional_variables,
    ]

    processor_tasks = []

    # get operation blocks
    settings = eyring13_recipe.processor_settings[variable["preprocessor"]]
    settings = {
        **get_default_settings(),
       **settings,
    }
    settings = update_levels(settings, work_dir, {
        "data_path": eyring13_config.data_path
    })

    blocks = generate_default_operation_blocks(
        "zonal",
        settings,
    )

    total_count = len(blocks)

    processor_tasks.append(get_combine_task(
        variables=tasks,
        variable=variable,
        block_index=total_count - 1,
    ))

    return processor_tasks


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case107/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    processor_tasks = []

    # add recipe_dataset_index
    exp_datasets = eyring13_recipe.exp_datasets
    variables = eyring13_recipe.variables

    # 观测数据
    variable_additional_datasets = eyring13_recipe.variable_additional_datasets
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
