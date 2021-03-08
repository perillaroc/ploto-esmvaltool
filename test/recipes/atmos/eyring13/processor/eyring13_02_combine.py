import itertools
from pathlib import Path

from ploto_esmvaltool.processor.esmvaltool_util_processor import run_processor
from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.util import (
    get_default_settings,
)
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.eyring13 import generate_default_operation_blocks
from ploto_esmvaltool.util.esmvaltool import (
    get_datasets
)

from test.recipes.atmos.eyring13 import (
    config as eyring13_config,
    recipe as eyring13_recipe,
)


diagnostic_name = "fig12"


def get_combine_task(
        variables,
        variable,
        block_index,
):
    task = {
        "util_type": "combine_metadata",
        "metadata_files": [
            "{work_dir}" + f"/{diagnostic_name}/processor/preproc/step-{block_index:02}/{d['alias']}/{d['variable_group']}/metadata.yml"
            for d in variables
        ],
        "output_directory": "{work_dir}" + f"/{diagnostic_name}/processor/preproc/{variable['variable_group']}",
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

    # get operation blocks
    settings = eyring13_recipe.processor_settings[variable["preprocessor"]]
    settings = {
        **get_default_settings(),
       **settings,
    }

    blocks = generate_default_operation_blocks(
        variable["preprocessor"],
        settings,
    )

    total_count = len(blocks)

    processor_tasks.append(get_combine_task(
        variables=tasks,
        variable=variable,
        block_index=total_count - 1,
    ))

    return processor_tasks


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case107/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    exp_datasets = eyring13_recipe.exp_datasets
    variables = eyring13_recipe.variables
    variable_additional_datasets = eyring13_recipe.variable_additional_datasets

    # get all datasets
    datasets = get_datasets(
        datasets=exp_datasets,
        variables=variables,
        variable_additional_datasets=variable_additional_datasets
    )

    processor_tasks = []
    for variable in variables:
        processor_tasks.extend(
            get_tasks_for_variable(
                variable=variable,
                datasets=datasets[variable["variable_group"]],
                config={
                    "data_path": eyring13_config.data_path
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
