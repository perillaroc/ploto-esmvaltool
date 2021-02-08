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

    short_name = variable["short_name"]

    task = {
        "dataset": dataset,
        "variables": variables,
        "data_path": climwip_config.data_path,

        "output_directory": "{work_dir}" + f"/{diagnostic_name}/fetcher/preproc/{dataset['dataset']}/{short_name}",
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


def get_weights_exp_processor(
        dataset,
        exp,
        variable,
        recipe_dataset_index,
        start_year,
        end_year,
        alias
):
    operations = generate_climatological_mean_operations()

    dataset = {
        "dataset": dataset,
        "project": "CMIP6",
        "mip": "Amon",
        "exp": exp,
        "ensemble": "r1i1p1f1",
        "grid": "gn",
        "frequency": "mon",
        "type": "exp",

        "start_year": start_year,
        "end_year": end_year,
    }

    diag_dataset = {
        "recipe_dataset_index": recipe_dataset_index,
        "alias": alias,
        "modeling_realm": [
            "atmos"
        ]
    }

    variable = variable

    diag = {
        "diagnostic": "calculate_weights_climwip",
    }

    settings = {
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

    task = {
        "input_data_source_file": "{work_dir}/weights/fetcher/preproc/"
                                  f"{dataset['dataset']}/{variable['short_name']}/data_source.yml",
        # output
        "output_directory": "{work_dir}" + f"/weights/processor/preproc/{dataset['dataset']}/{variable['short_name']}",

        # operations
        "operations": operations,

        "dataset": dataset,
        "diagnostic_dataset": diag_dataset,
        "variable": variable,
        "diagnostic": diag,
        "settings": settings,

        "step_type": "processor",
        "type": "ploto_esmvaltool.processor.esmvalcore_pre_processor",
    }

    return task



def get_weights_era5_processor(
        dataset,
        variable,
        recipe_dataset_index,
        start_year,
        end_year,
        alias
):
    operations = generate_climatological_mean_operations()

    dataset = {
        "dataset": dataset,
        "project": "native6",
        "type": "reanaly",
        "version": 1,
        "tier": 3,

        "mip": "Amon",
        "frequency": "mon",

        "start_year": start_year,
        "end_year": end_year,
    }

    diag_dataset = {
        "recipe_dataset_index": recipe_dataset_index,
        "alias": alias,
        "modeling_realm": [
            "atmos"
        ]
    }

    variable = variable

    diag = {
        "diagnostic": "calculate_weights_climwip",
    }

    settings = {
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

    task = {
        "input_data_source_file": "{work_dir}/weights/fetcher/preproc/"
                                  f"{dataset['dataset']}/{variable['short_name']}/data_source.yml",
        # output
        "output_directory": "{work_dir}" + f"/weights/processor/preproc/{dataset['dataset']}/{variable['short_name']}",

        # operations
        "operations": operations,

        "dataset": dataset,
        "diagnostic_dataset": diag_dataset,
        "variable": variable,
        "diagnostic": diag,
        "settings": settings,

        "step_type": "processor",
        "type": "ploto_esmvaltool.processor.esmvalcore_pre_processor",
    }
    return task


def get_weights_combine_task(short_name):
    task = {
        "util_type": "combine_metadata",
        "metadata_files": [
            "{work_dir}" + f"/weights/processor/preproc/FGOALS-g3/{short_name}/metadata.yml",
            "{work_dir}" + f"/weights/processor/preproc/CAMS-CSM1-0/{short_name}/metadata.yml",
            "{work_dir}" + f"/weights/processor/preproc/ERA5/{short_name}/metadata.yml"
        ],
        "output_directory": "{work_dir}" + f"/weights/processor/preproc/{short_name}",

        "step_type": "processor",
        "type": "ploto_esmvaltool.processor.esmvaltool_util_processor",
    }
    return task

def get_graph_exp_processor(
        dataset,
        exp,
        variable,
        recipe_dataset_index,
        start_year,
        end_year,
        alias
):
    operations = generate_temperature_anomalies_operations()

    dataset = {
        "dataset": dataset,
        "project": "CMIP6",
        "mip": "Amon",
        "exp": exp,
        "ensemble": "r1i1p1f1",
        "grid": "gn",
        "frequency": "mon",
        "type": "exp",  #*******************

        "start_year": start_year,
        "end_year": end_year,
    }

    diag_dataset = {
        "recipe_dataset_index": recipe_dataset_index,
        "alias": alias,
        "modeling_realm": [
            "atmos"
        ]
    }

    variable = variable

    diag = {
        "diagnostic": "weighted_temperature_graph",
    }

    settings = {}

    task = {
        "input_data_source_file": "{work_dir}/graph/fetcher/preproc/"
                                  f"{dataset['dataset']}/{variable['short_name']}/data_source.yml",
        # output
        "output_directory": "{work_dir}" + f"/graph/processor/preproc/{dataset['dataset']}/{variable['short_name']}",

        # operations
        "operations": operations,

        "dataset": dataset,
        "diagnostic_dataset": diag_dataset,
        "variable": variable,
        "diagnostic": diag,
        "settings": settings,

        "step_type": "processor",
        "type": "ploto_esmvaltool.processor.esmvalcore_pre_processor",
    }
    return task


def get_graph_combine_task(short_name):
    task = {
        "util_type": "combine_metadata",
        "metadata_files": [
            "{work_dir}" + f"/graph/processor/preproc/FGOALS-g3/{short_name}/metadata.yml",
            "{work_dir}" + f"/graph/processor/preproc/CAMS-CSM1-0/{short_name}/metadata.yml",
            ],
        "output_directory": "{work_dir}" + f"/graph/processor/preproc/{short_name}",

        "step_type": "processor",
        "type": "ploto_esmvaltool.processor.esmvaltool_util_processor",
    }
    return task


def get_map_tas_processor(
        dataset,
        exp,
        variable,
        recipe_dataset_index,
        start_year,
        end_year,
        alias
):
    operations = generate_climatological_mean_operations()

    dataset = {
        "dataset": dataset,
        "project": "CMIP6",
        "mip": "Amon",
        "exp": exp,
        "ensemble": "r1i1p1f1",
        "grid": "gn",
        "frequency": "mon",
        "type": "exp",  #*******************

        "start_year": start_year,
        "end_year": end_year,
    }

    diag_dataset = {
        "recipe_dataset_index": recipe_dataset_index,
        "alias": alias,
        "modeling_realm": [
            "atmos"
        ]
    }

    variable = variable

    diag = {
        "diagnostic": "weighted_temperature_map",
    }

    settings = {
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

    task = {
        "input_data_source_file": "{work_dir}/map/fetcher/preproc/"
                                  f"{dataset['dataset']}/{variable['variable_group']}/data_source.yml",
        # output
        "output_directory": "{work_dir}" + f"/map/processor/preproc/{dataset['dataset']}/{variable['variable_group']}",

        # operations
        "operations": operations,

        "dataset": dataset,
        "diagnostic_dataset": diag_dataset,
        "variable": variable,
        "diagnostic": diag,
        "settings": settings,

        "step_type": "processor",
        "type": "ploto_esmvaltool.processor.esmvalcore_pre_processor",
    }
    return task


def get_map_combine_task(variable_group):
    task = {
        "util_type": "combine_metadata",
        "metadata_files": [
            "{work_dir}" + f"/map/processor/preproc/FGOALS-g3/{variable_group}/metadata.yml",
            "{work_dir}" + f"/map/processor/preproc/CAMS-CSM1-0/{variable_group}/metadata.yml",
            ],
        "output_directory": "{work_dir}" + f"/map/processor/preproc/{variable_group}",

        "step_type": "processor",
        "type": "ploto_esmvaltool.processor.esmvaltool_util_processor",
    }
    return task


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
                                                 f"{combined_dataset['dataset']}/{combined_dataset['short_name']}/data_source.yml",
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
    return steps

    # STEP: graph
    variables = ["tas"]
    tasks = [
        {
            "dataset": d["name"],
            "exp": "historical-ssp585",
            "variable": {
                "short_name": v,
                "variable_group": v,
                "preprocessor": "temperature_anomalies",
            },
            "recipe_dataset_index": d["index"],
            "start_year": 1960,
            "end_year": 2099,
            "alias": d["name"]
        }
        for v, d in itertools.product(variables, datasets)
    ]
    steps.extend([get_graph_exp_processor(**task) for task in tasks])

    tasks = [
        get_graph_combine_task(short_name) for short_name in ["tas"]
    ]
    steps.extend(tasks)

    # STEP: map
    variables = ["tas"]
    tasks = [
        {
            "dataset": d["name"],
            "exp": "historical-ssp585",
            "variable": {
                "short_name": v,
                "variable_group": v,
                "preprocessor": "temperature_anomalies",
            },
            "recipe_dataset_index": d["index"],
            "start_year": 2081,
            "end_year": 2099,
            "alias": d["name"]
        }
        for v, d in itertools.product(variables, datasets)
    ]
    steps.extend([get_map_tas_processor(**task) for task in tasks])

    variables = ["tas"]
    tasks = [
        {
            "dataset": d["name"],
            "exp": "historical-ssp585",
            "variable": {
                "short_name": v,
                "variable_group": f"{v}_reference",
                "preprocessor": "temperature_anomalies",
            },
            "recipe_dataset_index": d["index"],
            "start_year": 1995,
            "end_year": 2014,
            "alias": d["name"]
        }
        for v, d in itertools.product(variables, datasets)
    ]
    steps.extend([get_map_tas_processor(**task) for task in tasks])

    tasks = [
        get_map_combine_task(variable_group) for variable_group in ["tas", "tas_reference"]
    ]
    steps.extend(tasks)

    return steps


def get_plotter_steps():
    steps = []

    plot_task = generate_calculate_weights_plot_task()
    task = {
        "step_type": "plotter",
        "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",
        **plot_task,
        "config": plot_config,
        "input_files": [
            "{work_dir}/weights/processor/preproc/tas/metadata.yml",
            "{work_dir}/weights/processor/preproc/pr/metadata.yml",
            "{work_dir}/weights/processor/preproc/psl/metadata.yml",
        ],
    }
    steps.append(task)

    plot_task = generate_weighted_temperature_graph_plot_task()
    task = {
        "step_type": "plotter",
        "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",
        **plot_task,
        "config": plot_config,
        "input_files": [
            "{work_dir}/weights/plotter/work/",
            "{work_dir}/graph/processor/preproc/tas/metadata.yml",
        ],
    }
    steps.append(task)

    plot_task = generate_weighted_temperature_map_plot_task()
    task = {
        "step_type": "plotter",
        "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",
        **plot_task,
        "config": climwip_config.plot_config,
        "input_files": [
            "{work_dir}/weights/plotter/work/",
            "{work_dir}/map/processor/preproc/tas/metadata.yml",
            "{work_dir}/map/processor/preproc/tas_reference/metadata.yml",
        ],
    }
    steps.append(task)

    return steps


def run_climwip():
    steps = []
    steps.extend(get_fetcher_steps())
    steps.extend(get_processor_steps())
    # steps.extend(get_plotter_steps())

    config = climwip_config.config
    Path(config["base"]["run_base_dir"]).mkdir(parents=True, exist_ok=True)

    run_ploto({
        "data": {
            "steps": steps
        }
    }, config)



if __name__ == "__main__":
    run_climwip()
