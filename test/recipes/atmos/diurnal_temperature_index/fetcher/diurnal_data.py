import itertools

from ploto_esmvaltool.fetcher.esmvalcore_fetcher import get_data

from test.recipes.atmos.diurnal_temperature_index import (
    config as diurnal_config,
    recipe as diurnal_recipe,
)

def run(
        exp_dataset,
        variable
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case102/ploto"

    combined_dataset = {
        **exp_dataset,
        **variable
    }

    variables = [
        variable
    ]

    data_path = diurnal_config.data_path

    task = {
        "dataset": combined_dataset,
        "variables": variables,
        "data_path": data_path,

        "output_directory": "{work_dir}" + f"/fetcher/preproc/{combined_dataset['alias']}/{variable['variable_group']}",
        "output_data_source_file": "data_source.yml",
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
