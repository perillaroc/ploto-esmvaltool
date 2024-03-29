import itertools

from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.diurnal_temperature_indicator import (
    generate_default_plot_task,
    generate_default_preprocessor_operations
)
from ploto_esmvaltool.util.esmvaltool import add_variable_info

from ploto.run import run_ploto

from test.recipes.atmos.diurnal_temperature_index import (
    config as diurnal_config,
    recipe as diurnal_recipe,
)


def run_dry_days():
    steps = []

    steps.extend(get_fetcher_tasks())
    steps.extend(get_processor_tasks())
    steps.extend(get_combine_metadata_tasks())
    steps.append(get_plotter_task())

    config = diurnal_config.config

    run_ploto({
        "data": {
            "steps": steps
        }
    }, config)


def get_fetcher(
        exp_dataset,
        variable
):
    combined_variable = {
        **exp_dataset,
        **variable
    }
    add_variable_info(combined_variable)

    data_path = diurnal_config.data_path

    task = {
        "products": [
            {
                "variable": combined_variable,
                "output": {
                    "output_directory": "{alias}/{variable_group}",
                    "output_data_source_file": "data_source.yml",
                }
            }
        ],
        "config": {
            "data_path": data_path,
        },
        "output": {
            "output_directory": "{work_dir}/fetcher/preproc",
        },

        "step_type": "fetcher",
        "type": "ploto_esmvaltool.fetcher.esmvalcore_fetcher"
    }
    return task


def get_fetcher_tasks():
    exp_datasets = diurnal_recipe.exp_datasets
    exp_datasets = [
        {
            **d,
            "alias": f"{d['dataset']}-{d['exp']}",
            "recipe_dataset_index": index
        }
        for index, d in enumerate(exp_datasets)
    ]
    variables = diurnal_recipe.variables

    tasks = [
        {
            "exp_dataset": d,
            "variable": v,
        }
        for d, v in itertools.product(exp_datasets, variables)
    ]
    return [get_fetcher(**task) for task in tasks]


def get_processor(
        exp_dataset,
        variable
):
    operations = generate_default_preprocessor_operations()

    combined_dataset = {
        **exp_dataset,
        **variable
    }

    diagnostic = {
        "diagnostic": "diurnal_temperature_indicator",
    }

    settings = diurnal_recipe.processor_settings[variable["preprocessor"]]

    task = {
        "products": [
            {
                "variable": combined_dataset,
                "input": {
                    "input_data_source_file": "{work_dir}/fetcher/preproc/{alias}/{variable_group}/data_source.yml",
                },
                "output": {
                    "output_directory": "{alias}/{variable_group}"
                },
                "settings": settings
            }
        ],

        # operations
        "operations": operations,

        "diagnostic": diagnostic,

        "output": {
            "output_directory": "{work_dir}/processor/preproc",
        },

        "step_type": "processor",
        "type": "ploto_esmvaltool.processor.esmvalcore_pre_processor"
    }
    return task


def get_processor_tasks():
    exp_datasets = diurnal_recipe.exp_datasets
    exp_datasets = [
        {
            **d,
            "alias": f"{d['dataset']}-{d['exp']}",
            "recipe_dataset_index": index
        }
        for index, d in enumerate(exp_datasets)
    ]
    variables = diurnal_recipe.variables

    tasks = [
        {
            "exp_dataset": d,
            "variable": v,
        }
        for d, v in itertools.product(exp_datasets, variables)
    ]
    return [get_processor(**task) for task in tasks]


def get_combine_metadata_tasks():
    exp_datasets = diurnal_recipe.exp_datasets
    exp_datasets = [
        {
            **d,
            "alias": f"{d['dataset']}-{d['exp']}",
            "recipe_dataset_index": index
        }
        for index, d in enumerate(exp_datasets)
    ]
    variables = diurnal_recipe.variables

    tasks = [
        {
            "util_type": "combine_metadata",
            "metadata_files": [
                "{work_dir}" + f"/processor/preproc/{d['alias']}/{v['variable_group']}/metadata.yml"
                for d in exp_datasets
            ],
            "output_directory": "{work_dir}" + f"/processor/preproc/{v['variable_group']}",

            "step_type": "processor",
            "type": "ploto_esmvaltool.processor.esmvaltool_util_processor"
        }
        for v in variables
    ]
    return tasks


def get_plotter_task():
    plot_task = generate_default_plot_task()
    task = {
        "step_type": "plotter",
        "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",

        "config": diurnal_config.plot_config,

        **plot_task,
        "input_files": [
            "{work_dir}" + f"/processor/preproc/{v['variable_group']}/metadata.yml"
            for v in diurnal_recipe.variables
        ],
    }
    return task


if __name__ == "__main__":
    run_dry_days()
