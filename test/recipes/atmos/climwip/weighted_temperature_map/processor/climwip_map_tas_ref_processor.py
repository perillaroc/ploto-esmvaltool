from pathlib import Path
import itertools

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.climwip import generate_climatological_mean_operations
from loguru import logger


def run(
        dataset,
        exp,
        variable,
        recipe_dataset_index,
        start_year,
        end_year,
        alias
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case105/ploto/map/processor"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

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
        "input_data_source_file": f"/home/hujk/ploto/esmvaltool/cases/case105/ploto/map/fetcher/preproc/"
                                  f"{dataset['dataset']}/{variable['variable_group']}/data_source.yml",
        # output
        "output_directory": f"{work_dir}/preproc/{dataset['dataset']}/{variable['variable_group']}",

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
    variables = ["tas"]
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

    for task in tasks:
        run(**task)


if __name__ == "__main__":
    main()
