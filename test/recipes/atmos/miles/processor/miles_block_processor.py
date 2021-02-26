from pathlib import Path
import itertools

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.miles import (
    generate_default_operations
)
from ploto_esmvaltool.util.esmvaltool import (
    combine_variable,
    add_variable_info,
)

from test.recipes.atmos.miles import (
    recipe as miles_recipe,
    config as miles_config,
)


def run(
        exp_dataset,
        variable,
        diagnostic_name
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case103/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    operations = generate_default_operations()

    combined_dataset = combine_variable(
        dataset=exp_dataset,
        variable=variable,
    )
    add_variable_info(combined_dataset)


    diagnostic = {
        "diagnostic": "diurnal_temperature_indicator",
    }

    settings = miles_recipe.processor_settings[combined_dataset["preprocessor"]]

    task = {
        "products": [
            {
                "variable": combined_dataset,
                "input": {
                    "input_data_source_file": (
                        "{work_dir}"
                        f"/{diagnostic_name}/fetcher/preproc"
                        "/{dataset}/{variable_group}/data_source.yml"
                    ),
                },
                "output": {
                    "output_directory": "{dataset}/{variable_group}"
                },
                "settings": settings
            }
        ],

        # operations
        "operations": operations,

        "diagnostic": diagnostic,

        "output": {
            "output_directory": "{work_dir}" + f"/{diagnostic_name}/processor/preproc",
        },
    }

    run_processor(
        task=task,
        work_dir=work_dir,
        config={},
    )


def main():
    exp_datasets = miles_recipe.exp_datasets
    datasets = [
        {
            **d,
            "recipe_dataset_index": index,
            "alias": d["dataset"]
        }
        for index, d in enumerate(exp_datasets)
    ]

    variables = miles_recipe.variables

    tasks = [
        {
            "exp_dataset": d,
            "variable": v,
            "diagnostic_name": "miles_block",
        }
        for d, v in itertools.product(datasets, variables)
    ]

    for task in tasks:
        run(**task)


if __name__ == "__main__":
    main()
