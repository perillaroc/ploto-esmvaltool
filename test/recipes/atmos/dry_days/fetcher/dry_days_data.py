import itertools

from ploto_esmvaltool.fetcher.esmvalcore_fetcher import get_data
from ploto_esmvaltool.util.esmvaltool import add_variable_info

from test.recipes.atmos.dry_days import recipe as dry_days_recipe
from test.recipes.atmos.dry_days import config as dry_days_config


def get_fetcher(
        exp_dataset,
        variable
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case101/ploto"

    combined_variable = {
        **exp_dataset,
        **variable
    }
    add_variable_info(combined_variable)

    data_path = dry_days_config.data_path

    task = {
        "products": [
            {
                "variable": combined_variable,
                "output": {
                    "output_directory": "{dataset}/{variable_group}",
                    "output_data_source_file": "data_source.yml",
                }
            }
        ],
        "output": {
            "output_directory": "{work_dir}/fetcher/preproc",
        },

        "config": {
            "data_path": data_path,
        },
    }

    config = {}

    get_data(
        task=task,
        work_dir=work_dir,
        config=config
    )


def main():
    datasets = dry_days_recipe.exp_datasets
    variables = dry_days_recipe.variables

    for d, v in itertools.product(datasets, variables):
        get_fetcher(d, v)


if __name__ == "__main__":
    main()
