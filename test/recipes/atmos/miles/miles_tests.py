from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.miles import (
    generate_default_plot_task,
    generate_default_preprocessor_operations,
)
from ploto.run import run_ploto


short_name = "zg"

start_year = 1980
end_year = 1985

common_dataset = {
    "frequency": "day",
    "mip": "day",

    "start_year": start_year,
    "end_year": end_year,
}

variable = {
    "short_name": short_name,
    "variable_group": short_name,
    "preprocessor": "preproc",
    "reference_dataset": "ERA-Interim",  # *****************
}

processor_settings = {
    "extract_region": {
        "start_longitude": 0,
        "end_longitude": 360,
        "start_latitude": -1.25,
        "end_latitude": 90,
    },
    "extract_levels": {
        "levels": 50000,
        "scheme": "linear"
    },
    "regrid": {
        "target_grid": "2.5x2.5",
        "scheme": "linear_extrapolate"
    }
}


exp = "historical"
exp_dataset = {
    "dataset": "FGOALS-g3",
    "project": "CMIP6",
    "exp": exp,
    "ensemble": "r1i1p1f1",
    "grid": "gn",
    "type": "exp",
}

reanaly_dataset = {
    "dataset": "ERA-Interim",
    "project": "OBS6",
    "type": "reanaly",
    "version": 1,
    "tier": 3,
}


data_path = {
    "CMIP6": [
        "/home/hujk/clusterfs/wangdp/data/CMIP6"
    ],
    "OBS6": [
        # "/home/hujk/clusterfs/wangdp/data/obs"
        "/data/brick/b2/OBS/esmvaltool_output/cmorize_obs_20210119_071639"
    ],
}


plot_config = {
    "log_level": "info",
    "write_netcdf": True,
    "write_plots": True,
    "output_file_type": "png",
    "profile_diagnostic": False,
    "auxiliary_data_dir": "/home/hujk/ploto/esmvaltool/cases/case1/case1.2/auxiliary_data"
}


def get_fetcher_steps():
    dataset = {
        **exp_dataset,
        **common_dataset
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

        "output_directory": "{work_dir}" + f"/preproc/{dataset['exp']}/{short_name}",
        "output_data_source_file": "data_source.yml",

        "step_type": "fetcher",
        "type": "ploto_esmvaltool.fetcher.esmvalcore_fetcher",
    }

    era_dataset = {
        **reanaly_dataset,
        **common_dataset
    }

    era_task = {
        "dataset": era_dataset,
        "variables": variables,
        "data_path": data_path,

        "output_directory": "{work_dir}" + f"/preproc/{era_dataset['dataset']}/{short_name}",
        "output_data_source_file": "data_source.yml",

        "step_type": "fetcher",
        "type": "ploto_esmvaltool.fetcher.esmvalcore_fetcher",
    }

    return [
        task,
        era_task
    ]


def get_processor_steps():
    operations = generate_default_preprocessor_operations()

    recipe_dataset_index = 0
    alias = "historical"

    dataset = {
        **exp_dataset,
        **common_dataset,
    }

    diagnostic_dataset = {
        "recipe_dataset_index": recipe_dataset_index,
        "alias": alias,
        "modeling_realm": [
            "atmos"
        ],
        "reference_dataset": "ERA-Interim"
    }

    diagnostic = {
        "diagnostic": "diurnal_temperature_indicator",
    }

    task = {
        "input_data_source_file": "{work_dir}" + f"/preproc/{dataset['exp']}/{variable['short_name']}/data_source.yml",
        # output
        "output_directory": "{work_dir}" + f"/preproc/{dataset['exp']}/{variable['short_name']}",

        # operations
        "operations": operations,

        "dataset": dataset,
        "diagnostic_dataset": diagnostic_dataset,
        "variable": variable,
        "diagnostic": diagnostic,
        "settings": processor_settings,

        "step_type": "processor",
        "type": "ploto_esmvaltool.processor.esmvalcore_pre_processor",
    }

    recipe_dataset_index = 1
    alias = "OBS6"

    era_dataset = {
        **reanaly_dataset,
        **common_dataset
    }

    diagnostic_dataset = {
        "recipe_dataset_index": recipe_dataset_index,
        "alias": alias,
        "modeling_realm": [
            "atmos"
        ],
        "reference_dataset": "ERA-Interim"
    }

    era_task = {
        "input_data_source_file": "{work_dir}" + f"/preproc/{era_dataset['dataset']}/{variable['short_name']}/data_source.yml",
        # output
        "output_directory": "{work_dir}" + f"/preproc/{era_dataset['dataset']}/{variable['short_name']}",

        # operations
        "operations": operations,

        "dataset": era_dataset,
        "diagnostic_dataset": diagnostic_dataset,
        "variable": variable,
        "diagnostic": diagnostic,
        "settings": processor_settings,

        "step_type": "processor",
        "type": "ploto_esmvaltool.processor.esmvalcore_pre_processor",
    }

    combine_task = {
        "util_type": "combine_metadata",
        "metadata_files": [
            "{work_dir}" + f"/preproc/{dataset['exp']}/{variable['short_name']}/metadata.yml",
            "{work_dir}" + f"/preproc/{era_dataset['dataset']}/{variable['short_name']}/metadata.yml"
        ],
        "output_directory": "{work_dir}/preproc/",

        "step_type": "processor",
        "type": "ploto_esmvaltool.processor.esmvaltool_util_processor",
    }

    return [
        task,
        era_task,
        combine_task
    ]


def get_plotter_steps():
    plot_task = generate_default_plot_task(script="miles_block")
    plot_task["diagnostic_script"]["settings"]["seasons"] = "DJF"

    block_task = {
        **plot_task,
        "config": plot_config,
        "input_files": [
            "{work_dir}/preproc/metadata.yml"
        ],

        "step_type": "plotter",
        "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",
    }

    plot_task = generate_default_plot_task(script="miles_eof")
    plot_task["diagnostic_script"]["settings"]["seasons"] = "DJF"
    plot_task["diagnostic_script"]["settings"]["teles"] = "NAO"

    eof_task = {
        "step_type": "plotter",
        "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",
        **plot_task,
        "config": plot_config,
        "input_files": [
            "{work_dir}/preproc/metadata.yml"
        ],
    }

    plot_task = generate_default_plot_task(script="miles_regimes")

    regime_task = {
        "step_type": "plotter",
        "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",
        **plot_task,
        "config": plot_config,
        "input_files": [
            "{work_dir}/preproc/metadata.yml"
        ],
    }

    return [
        block_task,
        eof_task,
        regime_task,
    ]


def run_miles_block():
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
            "run_base_dir": "/home/hujk/ploto/esmvaltool/cases/case3/run"
        }
    }

    run_ploto({
        "data": {
            "steps": steps
        }
    }, config)


if __name__ == "__main__":
    run_miles_block()
