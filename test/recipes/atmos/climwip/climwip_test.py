import itertools
from pathlib import Path

from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.climwip import (
    generate_default_operations,
    generate_default_plot_task
)
from ploto.run import run_ploto


from test.recipes.atmos.climwip import recipe as climwip_recipe
from test.recipes.atmos.climwip import config as climwip_config



def get_fetcher(
        exp_dataset,
        variable,
        diagnostic_name,
):
    dataset = {
        **exp_dataset,
        **variable
    }

    variables = [
        variable
    ]

    variable_group = variable["variable_group"]

    task = {
        "dataset": dataset,
        "variables": variables,
        "data_path": climwip_config.data_path,

        "output_directory": "{work_dir}" + f"/{diagnostic_name}/fetcher/preproc/{dataset['dataset']}/{variable_group}",
        "output_data_source_file": "data_source.yml",

        "step_type": "fetcher",
        "type": "ploto_esmvaltool.fetcher.esmvalcore_fetcher",
    }

    return task


def get_fetcher_steps():
    steps = []

    exp_datasets = climwip_recipe.exp_datasets
    obs_datasets = climwip_recipe.obs_datasets
    weights_variables = climwip_recipe.weights_variables

    tasks = [
        {
            "exp_dataset": d,
            "variable": v,
            "diagnostic_name": "weights"
        }
        for v, d in itertools.product(weights_variables, exp_datasets)
    ]
    steps.extend([get_fetcher(**task) for task in tasks])

    tasks = [
        {
            "exp_dataset": d,
            "variable": v,
            "diagnostic_name": "weights"
        }
        for v, d in itertools.product(weights_variables, obs_datasets)
    ]
    steps.extend([get_fetcher(**task) for task in tasks])

    graph_variables = climwip_recipe.graph_variables
    tasks = [
        {
            "exp_dataset": d,
            "variable": v,
            "diagnostic_name": "graph"
        }
        for v, d in itertools.product(graph_variables, exp_datasets)
    ]
    steps.extend([get_fetcher(**task) for task in tasks])


    map_variables = climwip_recipe.map_variables
    tasks = [
        {
            "exp_dataset": d,
            "variable": v,
            "diagnostic_name": "map"
        }
        for v, d in itertools.product(map_variables, exp_datasets)
    ]
    steps.extend([get_fetcher(**task) for task in tasks])

    return steps


def get_processor(
        exp_dataset,
        variable,
        settings,
        diagnostic_name,
        diagnostic,
        preprocessor_name,
):
    operations = generate_default_operations(preprocessor_name)

    combined_dataset = {
        **exp_dataset,
        **variable
    }

    diag_dataset = {
        "modeling_realm": [
            "atmos"
        ]
    }

    variable = variable

    diag = {
        "diagnostic": diagnostic,
    }

    task = {
        "input_data_source_file": "{work_dir}" + f"/{diagnostic_name}/fetcher/preproc/"
                                                 f"{combined_dataset['dataset']}/{combined_dataset['variable_group']}/data_source.yml",
        # output
        "output_directory": "{work_dir}" + f"/{diagnostic_name}/processor/preproc/{combined_dataset['dataset']}/{combined_dataset['variable_group']}",

        # operations
        "operations": operations,

        "dataset": combined_dataset,
        "diagnostic_dataset": diag_dataset,
        "variable": variable,
        "diagnostic": diag,
        "settings": settings,

        "step_type": "processor",
        "type": "ploto_esmvaltool.processor.esmvalcore_pre_processor",
    }
    return task


def get_combine_processor(
        datasets,
        variable,
        diagnostic_name,
):
    task = {
        "util_type": "combine_metadata",
        "metadata_files": [
            "{work_dir}" + f"/{diagnostic_name}/processor/preproc/{d['dataset']}/{variable['variable_group']}/metadata.yml"
            for d in datasets
        ],
        "output_directory": "{work_dir}" + f"/{diagnostic_name}/processor/preproc/{variable['variable_group']}",

        "step_type": "processor",
        "type": "ploto_esmvaltool.processor.esmvaltool_util_processor",
    }
    return task


def get_processor_steps():
    steps = []

    # STEP: weights
    weights_variables = climwip_recipe.weights_variables
    exp_datasets = climwip_recipe.exp_datasets
    exp_datasets = [
        {
            **d,
            "recipe_dataset_index": index,
            "alias": d["dataset"]
        }
        for index, d in enumerate(exp_datasets)
    ]

    obs_datasets = climwip_recipe.obs_datasets
    obs_datasets = [
        {
            **d,
            "recipe_dataset_index": index + len(exp_datasets),
            "alias": d["dataset"]
        }
        for index, d in enumerate(obs_datasets)
    ]

    weights_settings = {
        "mask_landsea": {
            "mask_out": "sea",
        },
        "regrid": {
            "target_grid": "2.5x2.5",
            "scheme": "linear"
        },
        "climate_statistics": {
            "operator": "mean"
        }
    }

    tasks = [
        {
            "exp_dataset": d,
            "variable": v,
            "settings": weights_settings,
            "diagnostic_name": "weights",
            "diagnostic": "calculate_weights_climwip",
            "preprocessor_name": "climatological_mean",
        }
        for v, d in itertools.product(weights_variables, exp_datasets)
    ]
    steps.extend([get_processor(**task) for task in tasks])

    tasks = [
        {
            "exp_dataset": d,
            "variable": v,
            "settings": weights_settings,
            "diagnostic_name": "weights",
            "diagnostic": "calculate_weights_climwip",
            "preprocessor_name": "climatological_mean",
        }
        for v, d in itertools.product(weights_variables, obs_datasets)
    ]
    steps.extend([get_processor(**task) for task in tasks])

    tasks = [
        {
            "datasets": [
                *exp_datasets,
                *obs_datasets,
            ],
            "variable": v,
            "diagnostic_name": "weights",
        }
        for v in weights_variables
    ]

    steps.extend([get_combine_processor(**task) for task in tasks])

    # STEP: graph
    graph_variables = climwip_recipe.graph_variables
    tasks = [
        {
            "exp_dataset": d,
            "variable": v,
            "settings": weights_settings,
            "diagnostic_name": "graph",
            "diagnostic": "weighted_temperature_graph",
            "preprocessor_name": "temperature_anomalies",
        }
        for v, d in itertools.product(graph_variables, exp_datasets)
    ]

    steps.extend([get_processor(**task) for task in tasks])

    tasks = [
        {
            "datasets": [
                *exp_datasets,
            ],
            "variable": v,
            "diagnostic_name": "graph",
        }
        for v in graph_variables
    ]
    steps.extend([get_combine_processor(**task) for task in tasks])

    # STEP: map
    map_variables = climwip_recipe.map_variables

    tasks = [
        {
            "exp_dataset": d,
            "variable": v,
            "settings": weights_settings,
            "diagnostic_name": "map",
            "diagnostic": "weighted_temperature_map",
            "preprocessor_name": "climatological_mean",
        }
        for v, d in itertools.product(map_variables, exp_datasets)
    ]
    steps.extend([get_processor(**task) for task in tasks])

    tasks = [
        {
            "datasets": [
                *exp_datasets,
            ],
            "variable": v,
            "diagnostic_name": "map",
        }
        for v in map_variables
    ]
    steps.extend([get_combine_processor(**task) for task in tasks])

    return steps


def get_plotter_steps():
    steps = []

    plot_task = generate_default_plot_task("calculate_weights_climwip")
    task = {
        "step_type": "plotter",
        "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",
        **plot_task,
        "config": climwip_config.plot_config,
        "input_files": [
            "{work_dir}" f"/weights/processor/preproc/{v['variable_group']}/metadata.yml"
            for v in climwip_recipe.weights_variables
        ],
    }
    steps.append(task)

    plot_task = generate_default_plot_task("weighted_temperature_graph")
    task = {
        "step_type": "plotter",
        "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",
        **plot_task,
        "config": climwip_config.plot_config,
        "input_files": [
            "{work_dir}/weights/plotter/work/",
            *[
                "{work_dir}" + f"/graph/processor/preproc/{v['variable_group']}/metadata.yml"
                for v in climwip_recipe.graph_variables
            ]
        ],
    }
    steps.append(task)

    plot_task = generate_default_plot_task("weighted_temperature_map")
    task = {
        "step_type": "plotter",
        "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",
        **plot_task,
        "config": climwip_config.plot_config,
        "input_files": [
            "{work_dir}/weights/plotter/work/",
            *[
                "{work_dir}" + f"/map/processor/preproc/{v['variable_group']}/metadata.yml"
                for v in climwip_recipe.map_variables
            ]
        ],
    }
    steps.append(task)

    return steps


def run_climwip():
    steps = []
    steps.extend(get_fetcher_steps())
    steps.extend(get_processor_steps())
    steps.extend(get_plotter_steps())

    config = climwip_config.config
    Path(config["base"]["run_base_dir"]).mkdir(parents=True, exist_ok=True)

    run_ploto({
        "data": {
            "steps": steps
        }
    }, config)


if __name__ == "__main__":
    run_climwip()
