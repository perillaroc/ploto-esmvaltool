from pathlib import Path
import itertools

from esmvalcore.preprocessor._derive import get_required

from ploto_esmvaltool.fetcher.esmvalcore_fetcher import get_data
from ploto_esmvaltool.util.esmvaltool import (
    combine_variable,
    add_variable_info
)

from test.recipes.atmos.eyring13 import (
    config as eyring13_config,
    recipe as eyring13_recipe,
)

diagnostic_name = "fig12"

def get_fetcher_tasks(
        exp_dataset,
        variable,
):
    # TODO: alias should use a function.
    #   dataset and exp may be in exp_dataset or variable.
    combined_variable = combine_variable(
        dataset=exp_dataset,
        variable=variable,
    )
    combined_variable["alias"] = f"{combined_variable['dataset']}-{combined_variable['exp']}"
    add_variable_info(combined_variable)

    tasks = []

    tasks.append({
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
            "data_path": eyring13_config.data_path,
        },

        "output": {
            "output_directory": "{work_dir}" + f"/{diagnostic_name}/fetcher/preproc",
        }
    })
    return tasks


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case107/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    exp_datasets = eyring13_recipe.exp_datasets
    variables = eyring13_recipe.variables


    # CMIP6数据
    tasks = [
        {
            "exp_dataset": d,
            "variable": v,
        }
        for v, d in itertools.product(variables, exp_datasets)
    ]

    fetcher_tasks = []
    for task in tasks:
        fetcher_tasks.extend(get_fetcher_tasks(**task))


    # 观测数据
    variable_additional_datasets = eyring13_recipe.variable_additional_datasets
    for variable in variables:
        if variable["variable_group"] in variable_additional_datasets:
            additional_datasets = variable_additional_datasets[variable["variable_group"]]
            additional_datasets = [{
                **d,
                "alias": f"{d['dataset']}-{d['project']}",
            } for d in additional_datasets]
            tasks = [
                {
                    "exp_dataset": {
                        **variable,
                        **d,
                    },
                    "variable": {},
                }
                for d in additional_datasets
            ]
            for task in tasks:
                fetcher_tasks.extend(get_fetcher_tasks(**task))

    for task in fetcher_tasks:
        get_data(
            task,
            config={},
            work_dir=work_dir
        )


if __name__ == "__main__":
    main()
