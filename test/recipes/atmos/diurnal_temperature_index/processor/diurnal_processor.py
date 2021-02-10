import itertools

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.diurnal_temperature_indicator import generate_default_preprocessor_operations

from test.recipes.atmos.diurnal_temperature_index import (
    config as diurnal_config,
    recipe as diurnal_recipe,
)


def run(
        exp_dataset,
        variable
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case102/ploto"
    operations = generate_default_preprocessor_operations()

    combined_dataset = {
        **exp_dataset,
        **variable
    }

    diag_dataset = {
        "modeling_realm": [
            "atmos"
        ],
    }

    variable = variable

    diag = {
        "diagnostic": "diurnal_temperature_indicator",
    }

    settings = diurnal_recipe.processor_settings[variable["preprocessor"]]

    task = {
        "input_data_source_file": "{work_dir}" + f"/fetcher/preproc/{combined_dataset['alias']}/{variable['variable_group']}/data_source.yml",
        # output
        "output_directory": "{work_dir}" + f"/processor/preproc/{combined_dataset['alias']}/{variable['variable_group']}",

        # operations
        "operations": operations,

        "dataset": combined_dataset,
        "diagnostic_dataset": diag_dataset,
        "variable": variable,
        "diagnostic": diag,
        "settings": settings
    }

    run_processor(
        task=task,
        work_dir=work_dir,
        config={},
    )


def main():
    exp_datasets = diurnal_recipe.exp_datasets
    exp_datasets = [
        {
            **d,
            "alias": f"{d['dataset']}-{d['exp']}",
            "recipe_dataset_index": index
        }
        for index, d in enumerate(exp_datasets)
    ]
    variables = diurnal_recipe.variables

    tasks = [
        {
            "exp_dataset": d,
            "variable": v,
        }
        for d, v in itertools.product(exp_datasets, variables)
    ]

    for task in tasks:
        run(**task)


if __name__ == "__main__":
    main()
