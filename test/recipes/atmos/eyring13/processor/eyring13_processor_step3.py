import itertools
from pathlib import Path

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.util import (
    get_default_settings,
    get_operation_blocks,
    MULTI_MODEL_FUNCTIONS
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


def get_processor_tasks(
        exp_datasets,
        variable,
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case107/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    processor_tasks = []

    diag = {
        "diagnostic": diagnostic_name,
    }

    def get_variable(exp_dataset, variable):
        combined_variable = combine_variable(
            dataset=exp_dataset,
            variable=variable,
        )
        combined_variable["alias"] = f"{combined_variable['dataset']}-{combined_variable['exp']}"
        add_variable_info(combined_variable)
        return combined_variable

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

    def get_product(d, variable):
        v = get_variable(
            exp_dataset=d,
            variable=variable,
        )
        return {
            "variable": v,
            "input": {
                "input_metadata_files": [
                    "{work_dir}"
                    f"/{diagnostic_name}/processor/preproc/step-02/{v['alias']}"
                    f"/{v['variable_group']}/metadata.yml"
                ]
            },
            "output": {
                "output_directory": "step-03/{alias}/{variable_group}",
            }
        }

    task = {
        "products": [
            get_product(d, variable) for d in exp_datasets
        ],

        # output
        "output": {
            "output_directory": "{work_dir}" + f"/{diagnostic_name}/processor/preproc"
        },

        # operations
        "operations": blocks[2],

        "diagnostic": diag,

        "settings": settings
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


    # get all tasks
    exp_tasks = [
        {
            **variable,
            **d,
        }
        for d in exp_datasets
    ]
    exp_tasks = [
        {
            **t,
            "alias": f"{t['dataset']}-{t['project']}",
        } for t in exp_tasks
    ]

    additional_tasks = [
        {
            **variable,
            **d,
        }
        for d in additional_datasets
    ]

    tasks = [
        *exp_tasks,
        *additional_tasks,
    ]

    processor_tasks = []

    # operations
    for task in tasks:
        processor_tasks.extend(get_processor_tasks(**task))


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case107/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    exp_datasets = eyring13_recipe.exp_datasets
    exp_datasets = [{
        **d,
        "recipe_dataset_index": index
    } for index, d in enumerate(exp_datasets)]
    current_index = len(exp_datasets)

    variables = eyring13_recipe.variables

    # 观测数据
    variable_additional_datasets = eyring13_recipe.variable_additional_datasets
    for variable in variables:
        if variable["variable_group"] in variable_additional_datasets:
            additional_datasets = variable_additional_datasets[variable["variable_group"]]
            variable_additional_datasets[variable["variable_group"]] = [{
                **d,
                "alias": f"{d['dataset']}-{d['project']}",
                "recipe_dataset_index": current_index + index
            } for index, d in enumerate(additional_datasets)]
            current_index += len(additional_datasets)

    processor_tasks = []

    for variable in variables:
        datasets = []
        datasets.extend(exp_datasets)

        if variable["variable_group"] in variable_additional_datasets:
            additional_datasets = variable_additional_datasets[variable["variable_group"]]
            datasets.extend(additional_datasets)

        # operations
        processor_tasks.extend(get_processor_tasks(
            exp_datasets=datasets,
            variable=variable
        ))

    for task in processor_tasks:
        run_processor(
            task,
            config={},
            work_dir=work_dir
        )


if __name__ == "__main__":
    main()
