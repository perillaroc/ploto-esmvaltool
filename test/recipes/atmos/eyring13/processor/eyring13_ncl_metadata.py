import itertools
from pathlib import Path

from ploto_esmvaltool.processor.esmvaltool_util_processor import run_processor
from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.util import (
    get_default_settings,
    is_multi_model_operation
)
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.eyring13 import generate_default_operation_blocks
from ploto_esmvaltool.util.esmvaltool import (
    combine_variable,
    add_variable_info
)

from test.recipes.atmos.eyring13 import (
    config as eyring13_config,
    recipe as eyring13_recipe,
)
from test.recipes.atmos.eyring13.util import update_levels


diagnostic_name = "fig12"


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
    settings = eyring13_recipe.processor_settings[variable["preprocessor"]]
    settings = {
        **get_default_settings(),
       **settings,
    }
    settings = update_levels(settings, work_dir, {
        "data_path": eyring13_config.data_path
    })

    blocks = generate_default_operation_blocks(
        "zonal",
        settings,
    )

    total_count = len(blocks)

    processor_tasks.append(get_ncl_metadata_task(
        variable=variable,
    ))

    return processor_tasks


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case107/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    processor_tasks = []

    variables = eyring13_recipe.variables
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
