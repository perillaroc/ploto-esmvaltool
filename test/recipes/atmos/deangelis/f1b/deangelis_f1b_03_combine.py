import itertools
from pathlib import Path

from ploto_esmvaltool.processor.esmvaltool_util_processor import run_processor
from ploto_esmvaltool.util.esmvaltool import (
    get_datasets
)

from test.recipes.atmos.deangelis import (
    config as deangelis_config,
    recipe as deangelis_recipe,
)


diagnostic_name = "f1b"


def get_combine_task(
        variables,
        variable,
):
    task = {
        "util_type": "combine_metadata",
        "products": [
            {
                "input": {
                    "input_metadata_files": [
                        "{work_dir}" + f"/{diagnostic_name}/processor/preproc/{d['alias']}/{d['variable_group']}/metadata.yml"
                        for d in variables
                    ],
                },
                "output": {
                    "output_directory": f"{variable['variable_group']}"
                }
            }
        ],
        "output": {
            "output_directory": "{work_dir}" + f"/{diagnostic_name}/processor/preproc",
        }
    }

    return task


def get_tasks_for_variable(
        variable,
        datasets,
        config,
        work_dir,
):
    tasks = datasets

    processor_tasks = []
    processor_tasks.append(get_combine_task(
        variables=tasks,
        variable=variable,
    ))

    return processor_tasks


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case106/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    exp_datasets = deangelis_recipe.f1b.exp_datasets
    variables = deangelis_recipe.f1b.variables

    # get all datasets
    datasets = get_datasets(
        datasets=exp_datasets,
        variables=variables,
    )

    processor_tasks = []
    for variable in variables:
        processor_tasks.extend(
            get_tasks_for_variable(
                variable=variable,
                datasets=datasets[variable["variable_group"]],
                config={
                    "data_path": deangelis_config.data_path
                },
                work_dir=work_dir,
            )
        )

    for task in processor_tasks:
        run_processor(
            task,
            config={},
            work_dir=work_dir
        )


if __name__ == "__main__":
    main()
