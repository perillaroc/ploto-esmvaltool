from pathlib import Path
import itertools

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.climwip import generate_default_operations

from test.recipes.atmos.climwip import recipe as climwip_recipe


def run(
        exp_dataset,
        variable
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case105/ploto/graph/processor"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    operations = generate_default_operations("temperature_anomalies")

    dataset = {
        **exp_dataset,
        **variable
    }

    diag_dataset = {
        "modeling_realm": [
            "atmos"
        ]
    }

    variable = variable

    diag = {
        "diagnostic": "weighted_temperature_graph",
    }

    settings = {}

    task = {
        "input_data_source_file": f"/home/hujk/ploto/esmvaltool/cases/case105/ploto/graph/fetcher/preproc/"
                                  f"{dataset['dataset']}/{variable['short_name']}/data_source.yml",
        # output
        "output_directory": f"{work_dir}/preproc/{dataset['dataset']}/{variable['short_name']}",

        # operations
        "operations": operations,

        "dataset": dataset,
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
    variables = climwip_recipe.graph_variables
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
