import pathlib

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.diurnal_temperature_indicator import generate_default_preprocessor_operations
from loguru import logger


def run(
        exp,
        variable,
        recipe_dataset_index,
        start_year,
        end_year,
        alias
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case2/ploto/processor"
    operations = generate_default_preprocessor_operations()

    dataset = {
            "dataset": "FGOALS-g3",
            "project": "CMIP6",
            "mip": "day",
            "exp": exp,
            "ensemble": "r1i1p1f1",
            "grid": "gn",
            "frequency": "day",

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
        "input_data_source_file": f"/home/hujk/ploto/esmvaltool/cases/case2/ploto/fetcher/preproc/{dataset['exp']}/{variable['short_name']}/data_source.yml",
        # output
        "output_directory": f"{work_dir}/preproc/{dataset['exp']}/{variable['short_name']}",

        # operations
        "operations": operations,

        "dataset": dataset,
        "diagnostic_dataset": diag_dataset,
        "variable": variable,
        "diagnostic": diag,
        "settings": settings
    }

    run_processor(
        task=task,
        work_dir=work_dir,
        config={},
    )


def main():
    tasks = [
        {
            "exp": "historical",
            "variable": {
                "short_name": "tasmax",
                "variable_group": "tasmax",
                "preprocessor": "preproc",
            },
            "recipe_dataset_index": 0,
            "start_year": 1980,
            "end_year": 1981,
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
            "start_year": 1980,
            "end_year": 1981,
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
            "start_year": 2030,
            "end_year": 2031,
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
            "start_year": 2030,
            "end_year": 2031,
            "alias": "ssp119"
        }
    ]
    for task in tasks:
        run(**task)


if __name__ == "__main__":
    main()
