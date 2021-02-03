from pathlib import Path

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.climwip import generate_climatological_mean_operations
from loguru import logger


def run(
        exp,
        variable,
        recipe_dataset_index,
        start_year,
        end_year,
        alias
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case105/ploto/processor"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    operations = generate_climatological_mean_operations()

    dataset = {
        "dataset": "FGOALS-g3",
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
        "input_data_source_file": f"/home/hujk/ploto/esmvaltool/cases/case105/ploto/fetcher/preproc/{dataset['exp']}/{variable['short_name']}/data_source.yml",
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
                "short_name": "tas",
                "variable_group": "tas",
                "preprocessor": "preproc",
            },
            "recipe_dataset_index": 0,
            "start_year": 1995,
            "end_year": 2014,
            "alias": "historical"
        },
    ]
    for task in tasks:
        run(**task)


if __name__ == "__main__":
    main()
