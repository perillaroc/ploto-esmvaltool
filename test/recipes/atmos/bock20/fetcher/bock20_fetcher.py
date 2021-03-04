from pathlib import Path

from ploto_esmvaltool.fetcher.esmvalcore_fetcher import get_data
from ploto_esmvaltool.util.esmvaltool import (
    combine_variable,
    add_variable_info
)

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
        variable,
        datasets,
        additional_datasets,
        work_dir,
):
    """
    recipe_dataset_index 仅在单个变量组内计数，各个变量组之间独立
    """
    # get recipe dataset index
    exp_datasets = [{
        **d,
        "recipe_dataset_index": index
    } for index, d in enumerate(datasets)]
    current_index = len(exp_datasets)

    additional_datasets = [{
        **d,
        "alias": f"{d['dataset']}-{d['project']}",
        "recipe_dataset_index": current_index + index
    } for index, d in enumerate(additional_datasets)]

    # get exp variables
    def generate_exp_variable(
            variable,
            dataset,
    ):
        v = combine_variable(
            variable=variable,
            dataset=dataset
        )
        add_variable_info(v)
        # TODO: alias should use a function.
        #   dataset and exp may be in exp_dataset or variable.
        v["alias"] = f"{v['dataset']}-{v['exp']}"
        return v

    exp_variables = [
        generate_exp_variable(variable=variable, dataset=d)
        for d in exp_datasets
    ]

    # get additional variables
    def generate_reference_variable(
            variable,
            dataset,
    ):
        v = combine_variable(
            variable=variable,
            dataset=dataset
        )
        add_variable_info(v)
        v["alias"] = f"{v['dataset']}-{v['project']}"
        return v

    additional_variables = [
        generate_reference_variable(
            variable=variable,
            dataset=d
        )
        for d in additional_datasets
    ]

    tasks = [
        *exp_variables,
        *additional_variables,
    ]

    fetcher_tasks = []
    for task in tasks:
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

    fetcher_tasks = []

    exp_datasets = bock20_recipe.exp_datasets
    variables = bock20_recipe.variables

    variable_additional_datasets = bock20_recipe.variable_additional_datasets
    for variable in variables:
        if variable["variable_group"] in variable_additional_datasets:
            additional_datasets = variable_additional_datasets[variable["variable_group"]]
        else:
            additional_datasets = []
        fetcher_tasks.extend(
            get_tasks_for_variable(
                variable=variable,
                datasets=exp_datasets,
                additional_datasets=additional_datasets,
                work_dir=work_dir
            )
        )

    for task in fetcher_tasks:
        get_data(
            task,
            config={},
            work_dir=work_dir
        )


if __name__ == "__main__":
    main()
