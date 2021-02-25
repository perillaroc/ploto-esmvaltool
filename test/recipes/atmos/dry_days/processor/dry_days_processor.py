import itertools

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.util.esmvaltool import (
    combine_variable,
    add_variable_info,
)
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.dry_days import generate_default_operations

from test.recipes.atmos.dry_days import (
    recipe as dry_days_recipe,
    config as dry_days_config
)


def get_processor(
        exp_dataset,
        variable
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case101/ploto"
    operations = generate_default_operations()

    combined_dataset = combine_variable(
        dataset=exp_dataset,
        variable=variable,
    )
    add_variable_info(combined_dataset)

    diagnostic = {
        "diagnostic": "dry_days",
    }

    task = {
        "products": [
            {
                "variable": combined_dataset,
                "input": {
                    "input_data_source_file": "{work_dir}/fetcher/preproc/{dataset}/{variable_group}/data_source.yml",
                },
                "output": {
                    "output_directory": "{dataset}/{variable_group}"
                }
            }
        ],

        # operations
        "operations": operations,

        "diagnostic": diagnostic,

        "output": {
            "output_directory": "{work_dir}/processor/preproc",
        },
    }

    run_processor(
        task=task,
        work_dir=work_dir,
        config={},
    )


def main():
    exp_datasets = dry_days_recipe.exp_datasets
    datasets = [
        {
            **d,
            "recipe_dataset_index": index,
            "alias": d["dataset"]
        }
        for index, d in enumerate(exp_datasets)
    ]

    variables = dry_days_recipe.variables

    for d, v in itertools.product(datasets, variables):
        get_processor(d, v)


if __name__ == "__main__":
    main()
