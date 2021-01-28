from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.consecdrydays import (
    generate_default_preprocessor_operations,
    generate_default_plot_task,
)
from ploto.run import run_ploto


def run_dry_days():
    steps = []

    dataset_1 = {
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

    dataset_2 = {
        "dataset": "FGOALS-g3",
        "project": "CMIP6",
        "mip": "day",
        "exp": "amip",
        "ensemble": "r1i1p1f1",
        "grid": "gn",
        "frequency": "day",

        "start_year": 1995,
        "end_year": 1996,
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

    steps.extend([
        {
            "step_type": "fetcher",
            "type": "ploto_esmvaltool.fetcher.esmvalcore_fetcher",
            **dataset_1,
            **variables,
            **data_path,
            "output_directory": "preproc/pr/1pctCO2",
            "output_data_source_file": "data_source.yml",
        },
        {
            "step_type": "fetcher",
            "type": "ploto_esmvaltool.fetcher.esmvalcore_fetcher",
            **dataset_2,
            **variables,
            **data_path,
            "output_directory": "preproc/pr/amip",
            "output_data_source_file": "data_source.yml",
        },
    ])

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

    steps.extend([
        {
            "step_type": "processor",
            "type": "ploto_esmvaltool.processor.esmvalcore_pre_processor",

            # input files
            "input_data_source_file": "preproc/pr/1pctCO2/data_source.yml",
            # output
            "output_directory": "preproc/pr/1pctCO2",
            "output_metadata_file_name": "metadata.yml",

            # operations
            "operations": operations,

            **dataset_1,
            **diag_dataset,
            **variable,
            **diag,
        },
        {

            "step_type": "processor",
            "type": "ploto_esmvaltool.processor.esmvalcore_pre_processor",

            # input files
            "input_data_source_file": "preproc/pr/amip/data_source.yml",
            # output
            "output_directory": "preproc/pr/amip",
            "output_metadata_file_name": "metadata.yml",

            # operations
            "operations": operations,

            **dataset_2,
            **diag_dataset,
            **variable,
            **diag,
        }
    ])

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
            "{work_dir}/preproc/pr/1pctCO2/metadata.yml",
            "{work_dir}/preproc/pr/amip/metadata.yml"
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
