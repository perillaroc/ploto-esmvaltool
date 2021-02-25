import itertools

from ploto_esmvaltool.fetcher.esmvalcore_fetcher import get_data
from ploto_esmvaltool.util.esmvaltool import add_variable_info

from test.recipes.atmos.diurnal_temperature_index import (
    config as diurnal_config,
    recipe as diurnal_recipe,
)

def run(
        exp_dataset,
        variable
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case102/ploto"

    combined_variable = {
        **exp_dataset,
        **variable
    }
    add_variable_info(combined_variable)

    data_path = diurnal_config.data_path

    task = {
        "products": [
            {
                "variable": combined_variable,
                "output": {
                    "output_directory": "{alias}/{variable_group}",
                    "output_data_source_file": "data_source.yml",
                }
            }
        ],
        "config": {
            "data_path": data_path,
        },
        "output": {
            "output_directory": "{work_dir}/fetcher/preproc",
        }
    }

    config = {}

    get_data(
        task=task,
        work_dir=work_dir,
        config=config
    )


def main():
    exp_datasets = diurnal_recipe.exp_datasets
    exp_datasets = [
        {
            **d,
            "alias": f"{d['dataset']}-{d['exp']}",
            "recipe_dataset_index": index
        }
        for index, d in enumerate(exp_datasets)
    ]
    variables = diurnal_recipe.variables

    tasks = [
        {
            "exp_dataset": d,
            "variable": v,
        }
        for d, v in itertools.product(exp_datasets, variables)
    ]

    for task in tasks:
        run(**task)

if __name__ == "__main__":
    main()
