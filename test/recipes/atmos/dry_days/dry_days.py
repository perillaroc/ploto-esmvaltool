from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.consecdrydays import (
    generate_default_preprocessor_operations,
    generate_default_plot_task,
)
from ploto.run import run_ploto


def run_dry_days():
    steps = []

    dataset = {
        "dataset": "FGOALS-g3",
        "project": "CMIP6",
        "mip": "day",
        "exp": "1pctCO2",
        "ensemble": "r1i1p1f1",
        "grid": "gn",
        "frequency": "day",

        "start_year": 370,
        "end_year": 371,
    }

    variables = {
        "variables": [
            {
                "short_name": "pr",
            }
        ]
    }

    data_path = {
        "data_path": {
            "CMIP6": [
                "/data/brick/b1/CMIP6_DATA/",
                "/data/brick/b0/CMIP6/",
            ]
        }
    }

    steps.append({
        "step_type": "fetcher",
        "type": "ploto_esmvaltool.fetcher.esmvalcore_fetcher",
        **dataset,
        **variables,
        **data_path,
        "output_directory": "preproc/pr",
        "output_data_source_file": "data_source.yml",
    })

    diag_dataset = {
        "recipe_dataset_index": 0,
        "alias": "FGOALS-g3",
        "modeling_realm": [
            "atmos"
        ],
    }

    variable = {
        "short_name": "pr",
        "variable_group": "pr",
        "preprocessor": "default",
    }

    diag = {
        "diagnostic": "dry_days",
    }
    operations = generate_default_preprocessor_operations()

    steps.append({
        "step_type": "processor",
        "type": "ploto_esmvaltool.processor.esmvalcore_pre_processor",

        # input files
        "input_data_source_file": "preproc/pr/data_source.yml",
        # output
        "output_directory": "preproc/pr",

        # operations
        "operations": operations,

        **dataset,
        **diag_dataset,
        **variable,
        **diag,
    })

    plot_task = generate_default_plot_task()
    steps.append({
        "step_type": "plotter",
        "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",
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
            "{work_dir}/preproc/pr/metadata.yml"
        ],
    })

    config = {
        "esmvaltool": {
            "executables": {
                "py": "/home/hujk/anaconda3/envs/wangdp-esm/bin/python"
            },
            "recipes": {
                "base": "/home/hujk/ploto/esmvaltool/study/esmvaltool/ESMValTool/esmvaltool/recipes",
            },
            "diag_scripts": {
                "base": "/home/hujk/ploto/esmvaltool/study/esmvaltool/ESMValTool/esmvaltool/diag_scripts",
            },
        },
        "base": {
            "run_base_dir": "/home/hujk/ploto/ploto-esmvaltool/dist/cases/case1/run"
        }
    }

    run_ploto({
        "data": {
            "steps": steps
        }
    }, config)


if __name__ == "__main__":
    run_dry_days()
