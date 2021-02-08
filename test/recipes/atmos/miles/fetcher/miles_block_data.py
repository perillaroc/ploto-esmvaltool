from pathlib import Path
import itertools

from ploto_esmvaltool.fetcher.esmvalcore_fetcher import get_data

from test.recipes.atmos.miles import recipe as miles_recipe
from test.recipes.atmos.miles import config as miles_config


def run(
    exp_dataset,
    variable,
    diagnostic_name
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case3/ploto/"
    Path(work_dir).mkdir(parents=True, exist_ok=True)


    combined_dataset = {
        **exp_dataset,
        **variable
    }

    variables = [
        variable
    ]

    task = {
        "dataset": combined_dataset,
        "variables": variables,
        "data_path": miles_config.data_path,

        "output_directory": f"{work_dir}/{diagnostic_name}/preproc/{combined_dataset['dataset']}/{combined_dataset['variable_group']}",
        "output_data_source_file": "data_source.yml",
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
