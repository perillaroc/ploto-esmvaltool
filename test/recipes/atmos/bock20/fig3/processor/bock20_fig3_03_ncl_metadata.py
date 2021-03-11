from pathlib import Path

from ploto_esmvaltool.processor.esmvaltool_util_processor import run_processor
from ploto_esmvaltool.util.esmvaltool import (
    get_datasets
)

from test.recipes.atmos.bock20 import (
    config as bock20_config,
    recipe as bock20_recipe,
)


diagnostic_name = "fig_3"


def get_ncl_metadata_task(
        variable,
):
    task = {
        "util_type": "write_ncl_metadata",
        "products": [
            {
                "input": {
                    "input_metadata_files": [
                        "{work_dir}" + f"/{diagnostic_name}/processor/preproc/{variable['variable_group']}/metadata.yml"
                    ]
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
        config,
        work_dir,
):
    processor_tasks = []
    processor_tasks.append(get_ncl_metadata_task(
        variable=variable,
    ))

    return processor_tasks


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case108/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    # recipe
    variables = bock20_recipe.fig3.variables
    variable_additional_datasets = bock20_recipe.fig3.variable_additional_datasets
    additional_datasets = bock20_recipe.fig3.additional_datasets

    # get all datasets
    datasets = get_datasets(
        variables=variables,
        variable_additional_datasets=variable_additional_datasets,
        additional_datasets=additional_datasets
    )


    processor_tasks = []
    for variable in variables:
        processor_tasks.extend(
            get_tasks_for_variable(
                variable=variable,
                config={
                    "data_path": bock20_config.data_path
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
