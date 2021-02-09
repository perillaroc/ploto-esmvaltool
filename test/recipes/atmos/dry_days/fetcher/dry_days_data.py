import itertools

from ploto_esmvaltool.fetcher.esmvalcore_fetcher import get_data

from test.recipes.atmos.dry_days import recipe as dry_days_recipe
from test.recipes.atmos.dry_days import config as dry_days_config


def run_processor(
        exp_dataset,
        variable
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case101/ploto"

    combined_dataset = {
        **exp_dataset,
        **variable
    }

    variables = [
        variable
    ]

    data_path = dry_days_config.data_path

    task = {
        "dataset": combined_dataset,
        "variables": variables,
        "data_path": data_path,

        "output_directory": "{work_dir}" + f"/fetcher/preproc/{combined_dataset['dataset']}/{variable['variable_group']}",
        "output_data_source_file": "data_source.yml",
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
        run_processor(d, v)


if __name__ == "__main__":
    main()
