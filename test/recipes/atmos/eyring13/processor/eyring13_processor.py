import itertools
from pathlib import Path

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
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
            }
        ],

        # output
        "output": {
            "output_directory": "{work_dir}" + f"/{diagnostic_name}/processor/preproc"
        },

        # operations
        "operations": operation_block,

        "diagnostic": diag,

        "settings": settings,
    }
    processor_tasks.append(task)

    return processor_tasks


def get_multi_model_processor_tasks(
        variables,
        operation_block,
        block_index,
        settings
):
    processor_tasks = []

    diag = {
        "diagnostic": diagnostic_name,
    }

    def get_product(variable):
        return {
            "variable": variable,
            "input": _get_input_section(block_index, variable),
            "output": _get_output_section(block_index, variable),
        }

    task = {
        "products": [
            get_product(variable) for variable in variables
        ],

        # output
        "output": {
            "output_directory": "{work_dir}" + f"/{diagnostic_name}/processor/preproc"
        },

        # operations
        "operations": operation_block,

        "diagnostic": diag,

        "settings": settings,
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

    # get processor tasks
    for block_index, operation_block in enumerate(blocks):
        if is_multi_model_operation(operation_block[0]):
            processor_tasks.extend(get_multi_model_processor_tasks(
                tasks,
                operation_block=operation_block,
                block_index=block_index,
                settings=settings
            ))
        else:
            for task in tasks:
                processor_tasks.extend(get_processor_tasks(
                    task,
                    operation_block=operation_block,
                    block_index=block_index,
                    settings=settings
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
