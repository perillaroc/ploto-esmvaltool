from pathlib import Path

from ploto_esmvaltool.fetcher.esmvalcore_fetcher import get_data
from ploto_esmvaltool.util.esmvaltool import (
    generate_variable
)
from ploto_esmvaltool.util.esmvaltool.datasets import set_alias

from test.recipes.atmos.bock20 import (
    config as bock20_config,
    recipe as bock20_recipe,
)


diagnostic_name = "fig_1_cmip6"


def get_fetcher_task(
        variable,
        config,
):
    task = {
        "products": [
            {
                "variable": variable,
                "output": {
                    "output_directory": "{alias}/{variable_group}",
                    "output_data_source_file": "data_source.yml",
                }
            }
        ],

        "config": config,

        "output": {
            "output_directory": "{work_dir}" + f"/{diagnostic_name}/fetcher/preproc",
        }
    }
    return task


def get_tasks_for_variable(
        datasets,
        work_dir,
):
    """
    recipe_dataset_index 仅在单个变量组内计数，各个变量组之间独立
    """
    fetcher_tasks = []
    for task in datasets:
        fetcher_tasks.append(
            get_fetcher_task(
                task,
                config={
                    "data_path": bock20_config.data_path
                }
            )
        )
    return fetcher_tasks


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case108/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    # recipe
    exp_datasets = bock20_recipe.exp_datasets
    variables = bock20_recipe.variables
    variable_additional_datasets = bock20_recipe.variable_additional_datasets

    # get all datasets
    datasets = {}
    for variable in variables:
        group_variables = []
        if variable["variable_group"] in variable_additional_datasets:
            additional_datasets = variable_additional_datasets[variable["variable_group"]]
        else:
            additional_datasets = []
        recipe_dataset_index = 0
        for d in [
            *exp_datasets,
            *additional_datasets
        ]:
            v = generate_variable(
                variable=variable,
                dataset=d,
            )
            v["recipe_dataset_index"] = recipe_dataset_index
            recipe_dataset_index += 1
            group_variables.append(v)
        datasets[variable["variable_group"]] = group_variables

    set_alias(datasets)

    # generate fetcher tasks
    fetcher_tasks = []
    for variable in variables:
        fetcher_tasks.extend(
            get_tasks_for_variable(
                datasets=datasets[variable["variable_group"]],
                work_dir=work_dir
            )
        )

    # run fetcher tasks
    for task in fetcher_tasks:
        get_data(
            task,
            config={},
            work_dir=work_dir
        )


if __name__ == "__main__":
    main()
