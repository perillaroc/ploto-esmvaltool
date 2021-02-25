from pathlib import Path
import itertools

from ploto_esmvaltool.fetcher.esmvalcore_fetcher import get_data
from ploto_esmvaltool.util.esmvaltool import add_variable_info

from test.recipes.atmos.miles import recipe as miles_recipe
from test.recipes.atmos.miles import config as miles_config


def run(
    exp_dataset,
    variable,
    diagnostic_name
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case103/ploto/"
    Path(work_dir).mkdir(parents=True, exist_ok=True)


    combined_dataset = {
        **exp_dataset,
        **variable
    }
    add_variable_info(combined_dataset)

    task = {
        "products": [
            {
                "variable": combined_dataset,
                "output": {
                    "output_directory": "{dataset}/{variable_group}",
                    "output_data_source_file": "data_source.yml",
                }
            }

        ],
        "output": {
            "output_directory": "{work_dir}" + f"/{diagnostic_name}/fetcher/preproc",
        },
        "config": {
            "data_path": miles_config.data_path,
        },
    }

    config = {}

    get_data(
        task=task,
        work_dir=work_dir,
        config=config
    )


def main():
    exp_datasets = miles_recipe.exp_datasets
    variables = miles_recipe.variables

    tasks = [
        {
            "exp_dataset": d,
            "variable": v,
            "diagnostic_name": "miles_block"
        }
        for d, v in itertools.product(exp_datasets, variables)
    ]

    for task in tasks:
        run(**task)

if __name__ == "__main__":
    main()
