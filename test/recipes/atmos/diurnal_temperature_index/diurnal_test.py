from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.diurnal_temperature_indicator import (
    generate_default_plot_task,
    generate_default_preprocessor_operations
)
from ploto.run import run_ploto


historical_start_year = 1961
historical_end_year = 1990
ssp119_start_year = 2030
ssp119_end_year = 2080

dataset_common = {
    "dataset": "FGOALS-g3",
    "project": "CMIP6",
    "mip": "day",
    "ensemble": "r1i1p1f1",
    "grid": "gn",
    "frequency": "day",
}


def run_dry_days():
    steps = []

    steps.extend(get_fetcher_tasks())
    steps.extend(get_processor_tasks())
    steps.extend(get_combine_metadata_tasks())
    steps.append(get_plotter_task())

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
            "run_base_dir": "/home/hujk/ploto/esmvaltool/cases/case2/run"
        }
    }

    run_ploto({
        "data": {
            "steps": steps
        }
    }, config)


def get_fetcher_task(
        exp,
        short_name,
        start_year,
        end_year
):
    dataset = {
        **dataset_common,

        "start_year": start_year,
        "end_year": end_year,
        "exp": exp,
    }

    variables = {
        "variables": [
            {
                "short_name": short_name,
            }
        ]
    }

    data_path = {
        "data_path": {
            "CMIP6": [
                "/home/hujk/clusterfs/wangdp/data/CMIP6"
            ]
        }
    }

    task = {
        **dataset,
        **variables,
        **data_path,

        "output_directory": "{work_dir}/preproc/" + f"{dataset['exp']}/{short_name}",
        "output_data_source_file": "data_source.yml",

        "step_type": "fetcher",
        "type": "ploto_esmvaltool.fetcher.esmvalcore_fetcher"
    }
    return task


def get_fetcher_tasks():
    tasks = [
        {
            "exp": "historical",
            "short_name": "tasmax",
            "start_year": historical_start_year,
            "end_year": historical_end_year
        },
        {
            "exp": "historical",
            "short_name": "tasmin",
            "start_year": historical_start_year,
            "end_year": historical_end_year
        },
        {
            "exp": "ssp119",
            "short_name": "tasmax",
            "start_year": ssp119_start_year,
            "end_year": ssp119_end_year
        },
        {
            "exp": "ssp119",
            "short_name": "tasmin",
            "start_year": ssp119_start_year,
            "end_year": ssp119_end_year
        }
    ]
    return [ get_fetcher_task(**task) for task in tasks]


def get_processor_task(
        exp,
        variable,
        recipe_dataset_index,
        start_year,
        end_year,
        alias
):
    operations = generate_default_preprocessor_operations()

    dataset = {
        **dataset_common,

        "exp": exp,
        "start_year": start_year,
        "end_year": end_year,
    }

    diag_dataset = {
        "recipe_dataset_index": recipe_dataset_index,
        "alias": alias,
        "modeling_realm": [
            "atmos"
        ],
    }

    variable = variable

    diag = {
        "diagnostic": "diurnal_temperature_indicator",
    }

    settings = {
            "extract_region": {
                "start_longitude": 70,
                "end_longitude": 140,
                "start_latitude": 15,
                "end_latitude": 55,
            },
            "mask_landsea": {
                "mask_out": "sea"
            }
    }

    task = {
        "input_data_source_file": "{work_dir}/preproc/" + f"{dataset['exp']}/{variable['short_name']}/data_source.yml",
        # output
        "output_directory": "{work_dir}/preproc/" + f"{dataset['exp']}/{variable['short_name']}",

        # operations
        "operations": operations,

        "dataset": dataset,
        "diagnostic_dataset": diag_dataset,
        "variable": variable,
        "diagnostic": diag,
        "settings": settings,

        "step_type": "processor",
        "type": "ploto_esmvaltool.processor.esmvalcore_pre_processor"
    }

    return task


def get_combine_metadata_tasks():
    short_names = [
        "tasmax",
        "tasmin",
    ]

    exps = [
        "historical",
        "ssp119"
    ]

    tasks = [{
        "util_type": "combine_metadata",
        "metadata_files": [
            "{work_dir}/preproc/" + f"{exp}/{short_name}/metadata.yml"
            for exp in exps
        ],
        "output_directory": "{work_dir}/preproc/" + f"{short_name}",

        "step_type": "processor",
        "type": "ploto_esmvaltool.processor.esmvaltool_util_processor"
    } for short_name in short_names ]

    return tasks


def get_processor_tasks():
    tasks = [
        {
            "exp": "historical",
            "variable": {
                "short_name": "tasmax",
                "variable_group": "tasmax",
                "preprocessor": "preproc",
            },
            "recipe_dataset_index": 0,
            "start_year": historical_start_year,
            "end_year": historical_end_year,
            "alias": "historical"
        },
        {
            "exp": "historical",
            "variable": {
                "short_name": "tasmin",
                "variable_group": "tasmin",
                "preprocessor": "preproc",
            },
            "recipe_dataset_index": 0,
            "start_year": historical_start_year,
            "end_year": historical_end_year,
            "alias": "historical"
        },
        {
            "exp": "ssp119",
            "variable": {
                "short_name": "tasmax",
                "variable_group": "tasmax",
                "preprocessor": "preproc",
            },
            "recipe_dataset_index": 1,
            "start_year": ssp119_start_year,
            "end_year": ssp119_end_year,
            "alias": "ssp119"
        },
        {
            "exp": "ssp119",
            "variable": {
                "short_name": "tasmin",
                "variable_group": "tasmin",
                "preprocessor": "preproc",
            },
            "recipe_dataset_index": 1,
            "start_year": ssp119_start_year,
            "end_year": ssp119_end_year,
            "alias": "ssp119"
        }
    ]
    return [ get_processor_task(**task) for task in tasks]


def get_plotter_task():
    plot_task = generate_default_plot_task()
    task = {
        **plot_task,
        "config": {
            "log_level": "info",
            "write_netcdf": True,
            "write_plots": True,
            "output_file_type": "png",
            "profile_diagnostic": False,
            "auxiliary_data_dir": "/home/hujk/ploto/esmvaltool/cases/case1/case1.2/auxiliary_data"
        },
        "input_files": [
            "{work_dir}/preproc/" + f"{short_name}/metadata.yml"
            for short_name in ["tasmax", "tasmin"]
        ],

        "step_type": "plotter",
        "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",
    }
    return task


if __name__ == "__main__":
    run_dry_days()
