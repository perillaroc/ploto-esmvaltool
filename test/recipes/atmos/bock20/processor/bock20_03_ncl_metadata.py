import itertools
from pathlib import Path

from ploto_esmvaltool.processor.esmvaltool_util_processor import run_processor
from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.util import (
    get_default_settings,
)
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.bock20 import generate_default_operation_blocks


from test.recipes.atmos.bock20 import (
    config as bock20_config,
    recipe as bock20_recipe,
)


diagnostic_name = "fig_1_cmip6"


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
        work_dir,
):
    processor_tasks = []

    # get operation blocks
    settings = bock20_recipe.processor_settings[variable["preprocessor"]]
    settings = {
        **get_default_settings(),
       **settings,
    }

    blocks = generate_default_operation_blocks(
        variable["preprocessor"],
        settings,
    )

    total_count = len(blocks)

    processor_tasks.append(get_ncl_metadata_task(
        variable=variable,
    ))

    return processor_tasks


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case108/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    processor_tasks = []

    variables = bock20_recipe.variables
    for variable in variables:
        processor_tasks.extend(
            get_tasks_for_variable(
                variable=variable,
                work_dir=work_dir
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
