from pathlib import Path

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.miles import (
    generate_default_operations
)
from loguru import logger


def run(
        exp,
        variable,
        recipe_dataset_index,
        start_year,
        end_year,
        alias
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case3/ploto/processor"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    operations = generate_default_operations()

    dataset = {
        "dataset": "FGOALS-g3",
        "project": "CMIP6",
        "mip": "day",
        "exp": exp,
        "ensemble": "r1i1p1f1",
        "grid": "gn",
        "frequency": "day",
        "type": "exp",  #*******************

        "start_year": start_year,
        "end_year": end_year,
    }

    diag_dataset = {
        "recipe_dataset_index": recipe_dataset_index,
        "alias": alias,
        "modeling_realm": [
            "atmos"
        ],
        "reference_dataset": "ERA-Interim"
    }

    variable = variable

    diag = {
        "diagnostic": "diurnal_temperature_indicator",
    }

    settings = {
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

    task = {
        "input_data_source_file": f"/home/hujk/ploto/esmvaltool/cases/case3/ploto/fetcher/preproc/{dataset['exp']}/{variable['short_name']}/data_source.yml",
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
                "short_name": "zg",
                "variable_group": "zg",
                "preprocessor": "preproc",
                "reference_dataset": "ERA-Interim", #*****************
            },
            "recipe_dataset_index": 0,
            "start_year": 1980,
            "end_year": 1985,
            "alias": "historical"
        },
    ]
    for task in tasks:
        run(**task)


if __name__ == "__main__":
    main()
