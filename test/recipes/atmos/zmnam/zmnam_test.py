"""
多模式仅是 metadata.yml 内容的叠加，与 dry_days 相同
"""
import itertools

from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.zmnam import (
    generate_default_plot_task,
    generate_default_operations,
)
from ploto.run import run_ploto

from test.recipes.atmos.zmnam import recipe as zmnam_recipe
from test.recipes.atmos.zmnam import config as zmnam_config


def get_fetcher(
        exp_dataset,
        variable
):
    combined_dataset = {
        **exp_dataset,
        **variable
    }

    variables = [
        variable
    ]

    data_path = zmnam_config.data_path

    task = {
        "dataset": combined_dataset,
        "variables": variables,
        "data_path": data_path,

        "output_directory": "{work_dir}" + f"/fetcher/preproc/{combined_dataset['alias']}/{variable['variable_group']}",
        "output_data_source_file": "data_source.yml",

        "step_type": "fetcher",
        "type": "ploto_esmvaltool.fetcher.esmvalcore_fetcher",
    }


    return task


def get_fetcher_steps():
    steps = []
    exp_datasets = zmnam_recipe.exp_datasets
    datasets = [
        {
            **d,
            "recipe_dataset_index": index,
            "alias": f"{d['dataset']}-{d['exp']}"
        }
        for index, d in enumerate(exp_datasets)
    ]

    variables = zmnam_recipe.variables

    tasks = [
        {
            "exp_dataset": d,
            "variable": v,
        } for d, v in itertools.product(datasets, variables)
    ]

    steps.extend([
        get_fetcher(**task) for task in tasks
    ])
    return steps


def get_processor(
        exp_dataset,
        variable
):
    operations = generate_default_operations()

    combined_dataset = {
        **exp_dataset,
        **variable,
    }

    diagnostic_dataset = {
        "modeling_realm": [
            "atmos"
        ],
    }

    diagnostic = {
        "diagnostic": "diurnal_temperature_indicator",
    }

    processor_settings = zmnam_recipe.processor_settings

    task = {
        "input_data_source_file": "{work_dir}" + f"/fetcher/preproc/{combined_dataset['alias']}/{variable['variable_group']}/data_source.yml",
        # output
        "output_directory": "{work_dir}" + f"/processor/preproc/{combined_dataset['alias']}/{variable['variable_group']}",

        # operations
        "operations": operations,

        "dataset": combined_dataset,
        "diagnostic_dataset": diagnostic_dataset,
        "variable": variable,
        "diagnostic": diagnostic,
        "settings": processor_settings,

        "step_type": "processor",
        "type": "ploto_esmvaltool.processor.esmvalcore_pre_processor",
    }
    return task


def get_processor_steps():
    steps = []
    exp_datasets = zmnam_recipe.exp_datasets
    datasets = [
        {
            **d,
            "recipe_dataset_index": index,
            "alias": f"{d['dataset']}-{d['exp']}"
        }
        for index, d in enumerate(exp_datasets)
    ]

    variables = zmnam_recipe.variables

    tasks = [
        {
            "exp_dataset": d,
            "variable": v,
        } for d, v in itertools.product(datasets, variables)
    ]
    steps.extend([
        get_processor(**task) for task in tasks
    ])

    combine_tasks = [
        {
            "util_type": "combine_metadata",
            "metadata_files": [
                "{work_dir}" + f"/processor/preproc/{d['alias']}/{v['variable_group']}/metadata.yml"
                for v in variables
            ],
            "output_directory": "{work_dir}" + f"/processor/preproc/{d['alias']}",

            "step_type": "processor",
            "type": "ploto_esmvaltool.processor.esmvaltool_util_processor",
        }
        for d in datasets
    ]
    steps.extend(combine_tasks)

    return steps


def get_plotter_steps():
    plot_task = generate_default_plot_task()

    exp_datasets = zmnam_recipe.exp_datasets
    datasets = [
        {
            **d,
            "recipe_dataset_index": index,
            "alias": f"{d['dataset']}-{d['exp']}"
        }
        for index, d in enumerate(exp_datasets)
    ]

    tasks = [
        {
            **plot_task,
            "config": zmnam_config.plot_config,
            "input_files": [
                "{work_dir}" + f"/processor/preproc/{d['alias']}/metadata.yml"
            ],
            "step_work_dir": "{work_dir}" + f"/plotter/{d['alias']}",

            "step_type": "plotter",
            "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",
        }
        for d in datasets
    ]
    return tasks


def run_miles_block():
    steps = []
    steps.extend(get_fetcher_steps())
    steps.extend(get_processor_steps())
    steps.extend(get_plotter_steps())

    config = zmnam_config.config

    run_ploto({
        "data": {
            "steps": steps
        }
    }, config)


if __name__ == "__main__":
    run_miles_block()
