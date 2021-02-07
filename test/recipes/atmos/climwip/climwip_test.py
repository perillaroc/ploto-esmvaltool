import itertools
from pathlib import Path

from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.climwip import (
    generate_climatological_mean_operations,
    generate_temperature_anomalies_operations
)
from ploto.run import run_ploto


data_path = {
    "CMIP6": [
        "/home/hujk/clusterfs/wangdp/data/CMIP6"
    ],
    "OBS6": [
        #"/home/hujk/clusterfs/wangdp/data/obs"
        "/data/brick/b2/OBS/esmvaltool_output/cmorize_obs_20210119_071639"
    ],
    "native6": [
        "/home/hujk/clusterfs/wangdp/data/rawobs"
    ]
}


def get_weights_fetcher(
        dataset,
        exp,
        start_year,
        end_year,
        short_name
):
    dataset = {
        "dataset": dataset,
        "project": "CMIP6",
        "mip": "Amon",
        "exp": exp,
        "ensemble": "r1i1p1f1",
        "grid": "gn",
        "frequency": "mon",

        "start_year": start_year,
        "end_year": end_year,
    }

    variables = [
        {
            "short_name": short_name,
        }
    ]

    task = {
        "dataset": dataset,
        "variables": variables,
        "data_path": data_path,

        "output_directory": "{work_dir}" + f"/weights/fetcher/preproc/{dataset['dataset']}/{short_name}",
        "output_data_source_file": "data_source.yml",

        "step_type": "fetcher",
        "type": "ploto_esmvaltool.fetcher.esmvalcore_fetcher",
    }
    return task


def get_weights_era5_fetcher(
        start_year,
        end_year,
        short_name
):
    dataset = {
        "dataset": "ERA5",
        "project": "native6",
        "type": "reanaly",
        "version": 1,
        "tier": 3,

        "mip": "Amip",
        "frequency": "mon",

        "start_year": start_year,
        "end_year": end_year,
    }

    variables = [
        {
            "short_name": short_name,
        }
    ]

    task = {
        "dataset": dataset,
        "variables": variables,
        "data_path": data_path,

        "output_directory": "{work_dir}" + f"/weights/fetcher/preproc/{dataset['dataset']}/{short_name}",
        "output_data_source_file": "data_source.yml",

        "step_type": "fetcher",
        "type": "ploto_esmvaltool.fetcher.esmvalcore_fetcher",
    }
    return task


def get_graph_fetcher(
        dataset,
        exp,
        start_year,
        end_year,
        short_name
):
    dataset = {
        "dataset": dataset,
        "project": "CMIP6",
        "mip": "Amon",
        "exp": exp,
        "ensemble": "r1i1p1f1",
        "grid": "gn",
        "frequency": "mon",

        "start_year": start_year,
        "end_year": end_year,
    }

    variables = [
        {
            "short_name": short_name,
        }
    ]

    task = {
        "dataset": dataset,
        "variables": variables,
        "data_path": data_path,

        "output_directory": "{work_dir}" + f"/graph/fetcher/preproc/{dataset['dataset']}/{short_name}",
        "output_data_source_file": "data_source.yml",

        "step_type": "fetcher",
        "type": "ploto_esmvaltool.fetcher.esmvalcore_fetcher",
    }

    return task


def get_map_tas_fetcher(
        dataset,
        exp,
        start_year,
        end_year,
        short_name
):
    dataset = {
        "dataset": dataset,
        "project": "CMIP6",
        "mip": "Amon",
        "exp": exp,
        "ensemble": "r1i1p1f1",
        "grid": "gn",
        "frequency": "mon",

        "start_year": start_year,
        "end_year": end_year,
    }

    variables = [
        {
            "short_name": short_name,
        }
    ]

    task = {
        "dataset": dataset,
        "variables": variables,
        "data_path": data_path,

        "output_directory": "{work_dir}" + f"/map/fetcher/preproc/{dataset['dataset']}/{short_name}",
        "output_data_source_file": "data_source.yml",

        "step_type": "fetcher",
        "type": "ploto_esmvaltool.fetcher.esmvalcore_fetcher",
    }
    return task


def get_map_tas_reference_fetcher(
        dataset,
        exp,
        short_name,
        variable_group,
        start_year,
        end_year
):
    dataset = {
        "dataset": dataset,
        "project": "CMIP6",
        "mip": "Amon",
        "exp": exp,
        "ensemble": "r1i1p1f1",
        "grid": "gn",
        "frequency": "mon",

        "start_year": start_year,
        "end_year": end_year,
    }

    variables = [
        {
            "short_name": short_name,
            "variable_group": variable_group
        }
    ]

    task = {
        "dataset": dataset,
        "variables": variables,
        "data_path": data_path,

        "output_directory": "{work_dir}" + f"/map/fetcher/preproc/{dataset['dataset']}/{variable_group}",
        "output_data_source_file": "data_source.yml",

        "step_type": "fetcher",
        "type": "ploto_esmvaltool.fetcher.esmvalcore_fetcher",
    }

    return task


def get_fetcher_steps():
    steps = []

    variables = ["tas", "psl", "pr"]
    datasets = ["FGOALS-g3", "CAMS-CSM1-0"]

    tasks = [
       {
            "dataset": d,
            "exp": ["historical", "ssp585"],
            "short_name": v,
            "start_year": 1995,
            "end_year": 2015
        }
        for v, d in itertools.product(variables, datasets)
    ]
    steps.extend([get_weights_fetcher(**task) for task in tasks])

    tasks = [
        {
            "short_name": v,
            "start_year": 1995,
            "end_year": 2014
        } for v in ["tas", "pr", "psl"]
    ]
    steps.extend([get_weights_era5_fetcher(**task) for task in tasks])

    tasks = [
        {
            "dataset": d,
            "exp": ["historical", "ssp585"],
            "short_name": "tas",
            "start_year": 1960,
            "end_year": 2099
        }
        for d in datasets
    ]
    steps.extend([get_graph_fetcher(**task) for task in tasks])


    variables = ["tas"]
    tasks = [
        {
            "dataset": d,
            "exp": ["historical", "ssp585"],
            "short_name": v,
            "start_year": 2081,
            "end_year": 2099
        }
        for v, d in itertools.product(variables, datasets)
    ]
    steps.extend([get_map_tas_fetcher(**task) for task in tasks])

    tasks = [
        {
            "dataset": d,
            "exp": ["historical", "ssp585"],
            "short_name": v,
            "variable_group": f"{v}_reference",
            "start_year": 1995,
            "end_year": 2014
        }
        for v, d in itertools.product(variables, datasets)
    ]
    steps.extend([get_map_tas_reference_fetcher(**task) for task in tasks])

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


def get_map_tas_reference_processor(
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


def get_processor_steps():
    steps = []

    variables = ["tas", "psl", "pr"]
    datasets = [
        {
            "name": "FGOALS-g3",
            "index": 0
        },
        {
            "name": "CAMS-CSM1-0",
            "index": 1
        }
    ]

    tasks = [
        {
            "dataset": d["name"],
            "exp": "historical-ssp585",
            "variable": {
                "short_name": v,
                "variable_group": f"{v}_CLIM",
                "preprocessor": "preproc",
            },
            "recipe_dataset_index": d["index"],
            "start_year": 1995,
            "end_year": 2014,
            "alias": d["name"]
        }
        for v, d in itertools.product(variables, datasets)
    ]
    steps.extend([get_weights_exp_processor(**task) for task in tasks])

    tasks = [
        {
            "dataset": "ERA5",
            "variable": {
                "short_name": v,
                "variable_group": f"{v}_CLIM",
                "preprocessor": "preproc",
            },
            "recipe_dataset_index": 2,
            "start_year": 1995,
            "end_year": 2014,
            "alias": "native6"
        } for v in ["tas", "pr", "psl"]
    ]
    steps.extend([get_weights_era5_processor(**task) for task in tasks])

    tasks = [
        get_weights_combine_task(short_name) for short_name in ["tas", "psl", "pr"]
    ]
    steps.extend(tasks)

    variables = ["tas"]
    # datasets = [
    #     {
    #         "name": "FGOALS-g3",
    #         "index": 0
    #     },
    #     {
    #         "name": "CAMS-CSM1-0",
    #         "index": 1
    #     }
    # ]

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

    variables = ["tas"]
    # datasets = [
    #     {
    #         "name": "FGOALS-g3",
    #         "index": 0
    #     },
    #     {
    #         "name": "CAMS-CSM1-0",
    #         "index": 1
    #     }
    # ]

    tasks = [
        {
            "dataset": d["name"],
            "exp": "historical-ssp585",
            "variable": {
                "short_name": v,
                "variable_group": v,
                "preprocessor": "climatological_mean",
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
                "preprocessor": "climatological_mean",
            },
            "recipe_dataset_index": d["index"],
            "start_year": 1995,
            "end_year": 2014,
            "alias": d["name"]
        }
        for v, d in itertools.product(variables, datasets)
    ]
    steps.extend([get_map_tas_reference_processor(**task) for task in tasks])

    tasks = [
        get_map_combine_task(variable_group) for variable_group in ["tas", "tas_reference"]
    ]
    steps.extend(tasks)

    return steps


def get_plotter_steps():
    steps = []
    return steps


def run_climwip():
    steps = []
    steps.extend(get_fetcher_steps())
    steps.extend(get_processor_steps())
    steps.extend(get_plotter_steps())

    config = {
        "esmvaltool": {
            "executables": {
                "py": "/home/hujk/anaconda3/envs/wangdp-esm/bin/python",
                "r": "/home/hujk/anaconda3/envs/wangdp-esm/bin/Rscript"
            },
            "recipes": {
                "base": "/home/hujk/ploto/esmvaltool/study/esmvaltool/ESMValTool/esmvaltool/recipes",
            },
            "diag_scripts": {
                "base": "/home/hujk/ploto/esmvaltool/study/esmvaltool/ESMValTool/esmvaltool/diag_scripts",
            },
        },
        "base": {
            "run_base_dir": "/home/hujk/ploto/esmvaltool/cases/case105/run"
        }
    }
    Path(config["base"]["run_base_dir"]).mkdir(parents=True, exist_ok=True)

    run_ploto({
        "data": {
            "steps": steps
        }
    }, config)



if __name__ == "__main__":
    run_climwip()
