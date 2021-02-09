"""
Notes
-----
多个数据集：

在 settings.yml 中的 input_files 添加多个 metadata.yml
"""
import itertools

from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.dry_days import (
    generate_default_operations,
    generate_default_plot_task,
)
from ploto.run import run_ploto

from test.recipes.atmos.dry_days import recipe as dry_days_recipe
from test.recipes.atmos.dry_days import config as dry_days_config


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

    data_path = dry_days_config.data_path

    task = {
        "dataset": combined_dataset,
        "variables": variables,
        "data_path": data_path,

        "output_directory": "{work_dir}" + f"/fetcher/preproc/{combined_dataset['dataset']}/{variable['variable_group']}",
        "output_data_source_file": "data_source.yml",

        "step_type": "fetcher",
        "type": "ploto_esmvaltool.fetcher.esmvalcore_fetcher",
    }
    return task


def get_processor(
        exp_dataset,
        variable
):
    operations = generate_default_operations()

    combined_dataset = {
        **exp_dataset,
        **variable
    }

    diag_dataset = {
        "modeling_realm": [
            "atmos"
        ],
    }

    diag = {
        "diagnostic": "dry_days",
    }

    task = {
        # input files
        "input_data_source_file": "{work_dir}" + f"/fetcher/preproc/{combined_dataset['dataset']}/{combined_dataset['variable_group']}/data_source.yml",
        # output
        "output_directory": "{work_dir}" + f"/processor/preproc/{combined_dataset['dataset']}/{combined_dataset['variable_group']}",

        # operations
        "operations": operations,

        "dataset": combined_dataset,
        "diagnostic_dataset": diag_dataset,
        "variable": variable,
        "diagnostic": diag,

        "step_type": "processor",
        "type": "ploto_esmvaltool.processor.esmvalcore_pre_processor",
    }
    return task


def run_dry_days():
    steps = []

    exp_datasets = dry_days_recipe.exp_datasets
    variables = dry_days_recipe.variables

    tasks = [
        {
            "exp_dataset": d,
            "variable": v,
        }
        for d, v in itertools.product(exp_datasets, variables)
    ]
    steps.extend([get_fetcher(**task) for task in tasks])

    datasets = [
        {
            **d,
            "recipe_dataset_index": index,
            "alias": d["dataset"]
        }
        for index, d in enumerate(exp_datasets)
    ]
    for d, v in itertools.product(datasets, variables):
        steps.append(get_processor(d, v))

    plot_task = generate_default_plot_task()
    steps.extend([
        {
            "step_type": "plotter",
            "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",

            **plot_task,
            "config": dry_days_config.plot_config,
            "input_files": [
                "{work_dir}" + f"/processor/preproc/{d['dataset']}/{v['variable_group']}/metadata.yml"
                for d in datasets
            ],
        }
        for v in variables
    ])

    config = dry_days_config.config

    run_ploto({
        "data": {
            "steps": steps
        }
    }, config)


if __name__ == "__main__":
    run_dry_days()
