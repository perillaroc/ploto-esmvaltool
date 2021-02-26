import itertools

from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.miles import (
    generate_default_plot_task,
    generate_default_operations,
)
from ploto_esmvaltool.util.esmvaltool import (
    combine_variable,
    add_variable_info,
)
from ploto.run import run_ploto

from test.recipes.atmos.miles import (
    recipe as miles_recipe,
    config as miles_config
)


def get_fetcher(
    exp_dataset,
    variable,
    diagnostic_name
):
    combined_dataset = {
        **exp_dataset,
        **variable
    }
    add_variable_info(combined_dataset)

    task = {
        "products": [
            {
                "variable": combined_dataset,
                "output": {
                    "output_directory": "{dataset}/{variable_group}",
                    "output_data_source_file": "data_source.yml",
                }
            }
        ],
        "output": {
            "output_directory": "{work_dir}" + f"/{diagnostic_name}/fetcher/preproc",
        },
        "config": {
            "data_path": miles_config.data_path,
        },

        "step_type": "fetcher",
        "type": "ploto_esmvaltool.fetcher.esmvalcore_fetcher",
    }

    return task


def get_fetcher_steps():
    exp_datasets = miles_recipe.exp_datasets
    variables = miles_recipe.variables

    tasks = [
        {
            "exp_dataset": d,
            "variable": v,
            "diagnostic_name": "miles_block"
        }
        for d, v in itertools.product(exp_datasets, variables)
    ]
    return [get_fetcher(**task) for task in tasks]


def get_processor(
        exp_dataset,
        variable,
        diagnostic_name
):
    operations = generate_default_operations()

    combined_dataset = combine_variable(
        dataset=exp_dataset,
        variable=variable,
    )
    add_variable_info(combined_dataset)

    diagnostic = {
        "diagnostic": "diurnal_temperature_indicator",
    }

    settings = miles_recipe.processor_settings[combined_dataset["preprocessor"]]

    task = {
        "products": [
            {
                "variable": combined_dataset,
                "input": {
                    "input_data_source_file": (
                        "{work_dir}"
                        f"/{diagnostic_name}/fetcher/preproc"
                        "/{dataset}/{variable_group}/data_source.yml"
                    ),
                },
                "output": {
                    "output_directory": "{dataset}/{variable_group}"
                },
                "settings": settings
            }
        ],

        # operations
        "operations": operations,

        "diagnostic": diagnostic,

        "output": {
            "output_directory": "{work_dir}" + f"/{diagnostic_name}/processor/preproc",
        },

        "step_type": "processor",
        "type": "ploto_esmvaltool.processor.esmvalcore_pre_processor",
    }
    return task


def get_combine_processor(
        exp_datasets,
        variables,
        diagnostic_name
):
    tasks = [
        {
            "util_type": "combine_metadata",
            "metadata_files": [
                "{work_dir}" + f"/{diagnostic_name}/processor/preproc/{d['dataset']}/{v['variable_group']}/metadata.yml"
                for d, v in itertools.product(exp_datasets, variables)
            ],
            "output_directory": "{work_dir}" + f"/{diagnostic_name}/processor/preproc/",

            "step_type": "processor",
            "type": "ploto_esmvaltool.processor.esmvaltool_util_processor",
        }
    ]
    return tasks


def get_processor_steps():
    steps = []
    exp_datasets = miles_recipe.exp_datasets
    datasets = [
        {
            **d,
            "recipe_dataset_index": index,
            "alias": d["dataset"]
        }
        for index, d in enumerate(exp_datasets)
    ]

    variables = miles_recipe.variables

    tasks = [
        {
            "exp_dataset": d,
            "variable": v,
            "diagnostic_name": "miles_block",
        }
        for d, v in itertools.product(datasets, variables)
    ]
    steps.extend([get_processor(**task) for task in tasks])

    steps.extend(get_combine_processor(datasets, variables, "miles_block"))

    return steps


def get_plotter_steps():
    steps = []
    diagnostic_name = "miles_block"

    plot_task = generate_default_plot_task(name=diagnostic_name)
    plot_task["diagnostic_script"]["settings"]["seasons"] = "DJF"

    task = {
        "step_type": "plotter",
        "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",

        **plot_task,
        "config": miles_config.plot_config,
        "input_files": [
            "{work_dir}" + f"/{diagnostic_name}/processor/preproc/metadata.yml"
        ],
    }
    steps.append(task)

    diagnostic_name = "miles_eof"
    data_diagnostic_name = "miles_block"

    plot_task = generate_default_plot_task(name=diagnostic_name)
    plot_task["diagnostic_script"]["settings"]["seasons"] = "DJF"
    plot_task["diagnostic_script"]["settings"]["teles"] = "NAO"

    task = {
        "step_type": "plotter",
        "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",

        **plot_task,
        "config": miles_config.plot_config,
        "input_files": [
            "{work_dir}" + f"/{data_diagnostic_name}/processor/preproc/metadata.yml"
        ],
    }
    steps.append(task)

    diagnostic_name = "miles_regimes"
    data_diagnostic_name = "miles_block"

    plot_task = generate_default_plot_task(name=diagnostic_name)

    task = {
        "step_type": "plotter",
        "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",

        **plot_task,
        "config": miles_config.plot_config,
        "input_files": [
            "{work_dir}" + f"/{data_diagnostic_name}/processor/preproc/metadata.yml"
        ],
    }
    steps.append(task)

    return steps


def run_miles_block():
    steps = []
    steps.extend(get_fetcher_steps())
    steps.extend(get_processor_steps())
    steps.extend(get_plotter_steps())

    config = miles_config.config

    run_ploto({
        "data": {
            "steps": steps
        }
    }, config)


if __name__ == "__main__":
    run_miles_block()
