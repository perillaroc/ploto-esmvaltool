from pathlib import Path
import itertools

from ploto_esmvaltool.fetcher.esmvalcore_fetcher import get_data
from ploto_esmvaltool.util.esmvaltool import (
    combine_variable,
    add_variable_info
)

from test.recipes.atmos.climwip import (
    recipe as climwip_recipe,
    config as climwip_config,
)

def run(
        exp_dataset,
        variable
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case105/ploto/weights/fetcher/"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    combined_variable = combine_variable(
        variable=variable,
        dataset=exp_dataset,
    )
    add_variable_info(combined_variable)

    data_path = climwip_config.data_path

    task = {
        "products": [
            {
                "variable": combined_variable,
                "output": {
                    "output_directory": "{dataset}/{short_name}",
                    "output_data_source_file": "data_source.yml",
                }
            }
        ],

        "output": {
            "output_directory": "{work_dir}/preproc"
        },

        "config": {
            "data_path": data_path,
        }
    }

    config = {}

    get_data(
        task=task,
        work_dir=work_dir,
        config=config
    )


def main():
    variables = climwip_recipe.weights_variables
    datasets = climwip_recipe.exp_datasets

    tasks = [
        {
            "exp_dataset": d,
            "variable": v,
        }
        for v, d in itertools.product(variables, datasets)
    ]

    for task in tasks:
        run(**task)

if __name__ == "__main__":
    main()
