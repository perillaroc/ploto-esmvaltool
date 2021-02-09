from pathlib import Path
import itertools

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.miles import (
    generate_default_operations
)

from test.recipes.atmos.miles import recipe as miles_recipe
from test.recipes.atmos.miles import config as miles_config


def run(
        exp_dataset,
        variable,
        diagnostic_name
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case103/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    operations = generate_default_operations()

    combined_dataset = {
        **exp_dataset,
        **variable
    }

    diag_dataset = {
        "modeling_realm": [
            "atmos"
        ]
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
        "input_data_source_file": f"{work_dir}/{diagnostic_name}/fetcher/preproc/{combined_dataset['dataset']}/{combined_dataset['variable_group']}/data_source.yml",
        # output
        "output_directory": f"{work_dir}/{diagnostic_name}/processor/preproc/{combined_dataset['dataset']}/{combined_dataset['variable_group']}",

        # operations
        "operations": operations,

        "dataset": combined_dataset,
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
    exp_datasets = miles_recipe.exp_datasets
    datasets = [
        {
            **d,
            "recipe_dataset_index": index,
            "alias": d["dataset"]
        }
        for index, d in enumerate(exp_datasets)
    ]

    variables = miles_recipe.variables

    tasks = [
        {
            "exp_dataset": d,
            "variable": v,
            "diagnostic_name": "miles_block",
        }
        for d, v in itertools.product(datasets, variables)
    ]

    for task in tasks:
        run(**task)


if __name__ == "__main__":
    main()
