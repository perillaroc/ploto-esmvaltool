from pathlib import Path
import itertools

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.climwip import generate_default_operations
from ploto_esmvaltool.util.esmvaltool import (
    combine_variable,
    add_variable_info
)

from test.recipes.atmos.climwip import (
    recipe as climwip_recipe,
    config as climwip_config,
)


diagnostic_name = "map"


def run(
        exp_dataset,
        variable,
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case105/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    combined_dataset = combine_variable(
        dataset=exp_dataset,
        variable=variable
    )
    add_variable_info(combined_dataset)

    diagnostic = {
        "diagnostic": "weighted_temperature_map",
    }

    settings = climwip_recipe.processor_settings[combined_dataset["preprocessor"]]
    operations = generate_default_operations(
        combined_dataset["preprocessor"],
        settings=settings
    )

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
                    "output_directory": "{alias}/{variable_group}"
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

        "step_type": "processor",
        "type": "ploto_esmvaltool.processor.esmvalcore_pre_processor",
    }

    run_processor(
        task=task,
        work_dir=work_dir,
        config={},
    )


def main():
    variables = climwip_recipe.map_variables
    datasets = climwip_recipe.exp_datasets
    datasets = [
        {
            **d,
            "recipe_dataset_index": index,
            "alias": d["dataset"]
        }
        for index, d in enumerate(datasets)
    ]

    tasks = [
        {
            "exp_dataset": d,
            "variable": v
        }
        for v, d in itertools.product(variables, datasets)
    ]

    for task in tasks:
        run(**task)


if __name__ == "__main__":
    main()
