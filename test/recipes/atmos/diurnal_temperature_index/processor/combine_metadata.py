import itertools

from ploto_esmvaltool.processor.esmvaltool_util_processor import run_processor

from test.recipes.atmos.diurnal_temperature_index import (
    config as diurnal_config,
    recipe as diurnal_recipe,
)


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case102/ploto"

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
            "util_type": "combine_metadata",
            "metadata_files": [
                "{work_dir}" + f"/processor/preproc/{d['alias']}/{v['variable_group']}/metadata.yml"
                for d in exp_datasets
            ],
            "output_directory": "{work_dir}" + f"/processor/preproc/{v['variable_group']}"
        } for v in variables
    ]

    for task in tasks:
        run_processor(
            task=task,
            work_dir=work_dir,
            config={}
        )


if __name__ == "__main__":
    main()
