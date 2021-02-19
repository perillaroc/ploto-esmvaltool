import itertools
from pathlib import Path

from ploto_esmvaltool.processor.esmvaltool_util_processor import run_processor

from test.recipes.atmos.deangelis import (
    config as deangelis_config,
    recipe as deangelis_recipe,
)


def get_combined_task(
        exp_datasets,
        variable,
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case106/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    processor_tasks = []

    variable_group = variable["variable_group"]
    task = {
        "util_type": "combine_metadata",
        "metadata_files": [
            "{work_dir}" + f"/processor/preproc/{d['alias']}/{variable_group}/metadata.yml"
            for d in exp_datasets
        ],
        "output_directory": "{work_dir}" + f"/processor/preproc/{variable_group}"
    }
    return task


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case106/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    exp_datasets = deangelis_recipe.exp_datasets
    exp_datasets = [{
        **d,
        "alias": f"{d['dataset']}-{d['exp']}",
    } for d in exp_datasets]
    variables = deangelis_recipe.variables

    tasks = [
        {
            "exp_datasets": exp_datasets,
            "variable": v,
        }
        for v in variables
    ]

    processor_tasks = []
    for task in tasks:
        processor_tasks.append(get_combined_task(**task))

    for task in processor_tasks:
        run_processor(
            task,
            config={},
            work_dir=work_dir
        )


if __name__ == "__main__":
    main()
