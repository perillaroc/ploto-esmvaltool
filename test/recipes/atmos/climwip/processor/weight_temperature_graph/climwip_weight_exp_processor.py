from pathlib import Path
import itertools

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.climwip import generate_temperature_anomalies_operations
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
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case105/ploto/processor/graph"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

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
        "input_data_source_file": f"/home/hujk/ploto/esmvaltool/cases/case105/ploto/fetcher/graph/preproc/"
                                  f"{dataset['dataset']}/{variable['short_name']}/data_source.yml",
        # output
        "output_directory": f"{work_dir}/preproc/{dataset['dataset']}/{variable['short_name']}",

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
            "exp": ["historical", "ssp585"],
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

    for task in tasks:
        run(**task)


if __name__ == "__main__":
    main()
