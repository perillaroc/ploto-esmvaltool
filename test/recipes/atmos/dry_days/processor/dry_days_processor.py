import itertools

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.dry_days import generate_default_operations


from test.recipes.atmos.dry_days import recipe as dry_days_recipe
from test.recipes.atmos.dry_days import config as dry_days_config


def get_processor(
        exp_dataset,
        variable
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case101/ploto"
    operations = generate_default_operations()

    combined_dataset = {
        **exp_dataset,
        **variable
    }

    diag_dataset = {
        "modeling_realm": [
            "atmos"
        ],
    }

    diag = {
        "diagnostic": "dry_days",
    }

    task = {
        # input files
        "input_data_source_file": f"{work_dir}/fetcher/preproc/{combined_dataset['dataset']}/{combined_dataset['variable_group']}/data_source.yml",
        # output
        "output_directory": f"{work_dir}/processor/preproc/{combined_dataset['dataset']}/{combined_dataset['variable_group']}",

        # operations
        "operations": operations,

        "dataset": combined_dataset,
        "diagnostic_dataset": diag_dataset,
        "variable": variable,
        "diagnostic": diag,
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
