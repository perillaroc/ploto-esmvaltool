"""
多模式仅是 metadata.yml 内容的叠加，与 dry_days 相同
"""

from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.zmnam import (
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

# variable

variable = {
    "short_name": short_name,
    "variable_group": short_name,

    "preprocessor": "preproc",
}

# processor

processor_settings = {
    "extract_region": {
        "start_longitude": 0,
        "end_longitude": 360,
        "start_latitude": 20,
        "end_latitude": 90,
    },
    "extract_levels": {
        "levels": [85000., 50000., 25000., 5000.],
        "scheme": "nearest"
    },
    "regrid": {
        "target_grid": "3x3",
        "scheme": "area_weighted"
    }
}

# datasets

exp = "amip"
exp_dataset = {
    "dataset": "FGOALS-g3",
    "project": "CMIP6",
    "exp": exp,
    "ensemble": "r1i1p1f1",
    "grid": "gn",
    "type": "exp",
}


# config

data_path = {
    "CMIP6": [
        "/data/brick/b1/CMIP6_DATA"
    ]
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


    return [
        task
    ]


def get_processor_steps():
    operations = generate_default_preprocessor_operations()

    recipe_dataset_index = 0
    alias = "amip"

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

    combine_task = {
        "util_type": "combine_metadata",
        "metadata_files": [
            "{work_dir}" + f"/preproc/{dataset['exp']}/{variable['short_name']}/metadata.yml",
        ],
        "output_directory": "{work_dir}/preproc/",

        "step_type": "processor",
        "type": "ploto_esmvaltool.processor.esmvaltool_util_processor",
    }

    return [
        task,
        combine_task
    ]


def get_plotter_steps():
    plot_task = generate_default_plot_task()

    task = {
        **plot_task,
        "config": plot_config,
        "input_files": [
            "{work_dir}/preproc/metadata.yml"
        ],

        "step_type": "plotter",
        "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",
    }
    return [
        task,
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
            "run_base_dir": "/home/hujk/ploto/esmvaltool/cases/case4/run"
        }
    }

    run_ploto({
        "data": {
            "steps": steps
        }
    }, config)


if __name__ == "__main__":
    run_miles_block()
