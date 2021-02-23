import itertools
from pathlib import Path

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.eyring13 import (
    generate_default_operations
)

from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.util import (
    split_derive_settings,
    get_operations,
    get_default_settings,
    get_operation_blocks
)


from test.recipes.atmos.eyring13 import (
    config as eyring13_config,
    recipe as eyring13_recipe,
)
from test.recipes.atmos.eyring13.util import update_levels


diagnostic_name = "fig12"

def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case107/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    exp_datasets = eyring13_recipe.exp_datasets
    exp_datasets = [{
        **d,
        "recipe_dataset_index": index
    } for index, d in enumerate(exp_datasets)]
    current_index = len(exp_datasets)

    variables = eyring13_recipe.variables

    tasks = [
        {
            "exp_dataset": d,
            "variable": v,
        }
        for v, d in itertools.product(variables, exp_datasets)
    ]

    blocks = get_operation_blocks(
        {
            **get_default_settings(),
            **eyring13_recipe.processor_settings["zonal"]
        }
    )
    for block in blocks:
        print(block)


if __name__ == "__main__":
    main()
