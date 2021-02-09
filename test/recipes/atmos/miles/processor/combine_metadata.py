import itertools

from ploto_esmvaltool.processor.esmvaltool_util_processor import run_processor

from test.recipes.atmos.miles import recipe as miles_recipe
from test.recipes.atmos.miles import config as miles_config


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case103/ploto"
    diagnostic_name = "miles_block"

    tasks = [
        {
            "util_type": "combine_metadata",
            "metadata_files": [
                f"{work_dir}/{diagnostic_name}/processor/preproc/{d['dataset']}/{v['variable_group']}/metadata.yml"
                for d, v in itertools.product(miles_recipe.exp_datasets, miles_recipe.variables)
            ],
            "output_directory": f"{work_dir}/{diagnostic_name}/processor/preproc/"
        }
    ]

    for task in tasks:
        run_processor(
            task=task,
            work_dir=work_dir,
            config={}
        )


if __name__ == "__main__":
    main()
