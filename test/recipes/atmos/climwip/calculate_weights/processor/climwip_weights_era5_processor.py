from pathlib import Path
import itertools

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.climwip import generate_default_operations

from test.recipes.atmos.climwip import recipe as climwip_recipe


def run(
        obs_dataset,
        variable
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case105/ploto/weights/processor"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    operations = generate_default_operations("climatological_mean")

    combined_dataset = {
        **obs_dataset,
        **variable
    }

    diag_dataset = {
        # "recipe_dataset_index": recipe_dataset_index,
        # "alias": alias,
        "modeling_realm": [
            "atmos"
        ]
    }

    variable = variable

    diag = {
        "diagnostic": "calculate_weights_climwip",
    }

    settings = {
        "mask_landsea": {
            "mask_out": "sea",
        },
        "regrid": {
            "target_grid": "2.5x2.5",
            "scheme": "linear"
        },
        "climate_statistics": {
            "operator": "mean"
        }
    }

    task = {
        "input_data_source_file": f"/home/hujk/ploto/esmvaltool/cases/case105/ploto/weights/fetcher/preproc/"
                                  f"{combined_dataset['dataset']}/{combined_dataset['short_name']}/data_source.yml",
        # output
        "output_directory": f"{work_dir}/preproc/{combined_dataset['dataset']}/{combined_dataset['variable_group']}",

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
    variables = climwip_recipe.weights_variables
    datasets = climwip_recipe.obs_datasets
    datasets = [
        {
            **d,
            "recipe_dataset_index": index + 2,
            "alias": d["dataset"]
        }
        for index, d in enumerate(datasets)
    ]

    tasks = [
        {
            "obs_dataset": d,
            "variable": v
        }
        for v, d in itertools.product(variables, datasets)
    ]

    for task in tasks:
        run(**task)


if __name__ == "__main__":
    main()
