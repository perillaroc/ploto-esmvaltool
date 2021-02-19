from pathlib import Path
import itertools

from esmvalcore.preprocessor._derive import get_required

from ploto_esmvaltool.fetcher.esmvalcore_fetcher import get_data

from test.recipes.atmos.deangelis import (
    config as deangelis_config,
    recipe as deangelis_recipe,
)

diagnostic_name = "f1b"

def get_fetcher_tasks(
        exp_dataset,
        variable,
):
    combined_variable = {
        **exp_dataset,
        **variable,
    }

    tasks = []

    if not combined_variable["derive"]:
        tasks.append({
            "dataset": combined_variable,
            "variables": [variable],
            "data_path": deangelis_config.data_path,

            "output_directory": "{work_dir}" + f"/{diagnostic_name}/fetcher/preproc/{combined_variable['alias']}/{combined_variable['variable_group']}",
            "output_data_source_file": "data_source.yml",
        })
    else:
        # 需要的变量，来自 ESMValCore
        required_variables = get_required(
            short_name=combined_variable["short_name"],
            project=combined_variable["project"]
        )

        # 输入变量
        input_variables = [{
            **combined_variable,
            **v,
            "variable_group": f"{combined_variable['short_name']}_derive_input_{v['short_name']}",
        } for v in required_variables]

        for v in input_variables:
            data_path = deangelis_config.data_path

            task = {
                "dataset": v,
                "variables": [v],
                "data_path": data_path,

                "output_directory": "{work_dir}" + f"/{diagnostic_name}/fetcher/preproc/{v['alias']}/{v['variable_group']}",
                "output_data_source_file": "data_source.yml",
            }

            tasks.append(task)

    return tasks


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case106/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    exp_datasets = deangelis_recipe.f1b.exp_datasets
    exp_datasets = [{
        **d,
        "alias": f"{d['dataset']}-{d['exp']}",
    } for d in exp_datasets]
    variables = deangelis_recipe.f1b.variables

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

    for task in fetcher_tasks:
        get_data(
            task,
            config={},
            work_dir=work_dir
        )




if __name__ == "__main__":
    main()
