from pathlib import Path
import itertools

from ploto_esmvaltool.fetcher.esmvalcore_fetcher import get_data

from test.recipes.atmos.climwip import recipe as climwip_recipe


def run(
        exp_dataset,
        variable,
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case105/ploto/graph/fetcher"
    Path(work_dir).mkdir(parents=True, exist_ok=True)


    dataset = {
        **exp_dataset,
        **variable
    }

    variables = [
        variable
    ]

    data_path = {
        "CMIP6": [
            "/home/hujk/clusterfs/wangdp/data/CMIP6"
        ]
    }

    short_name = variable["short_name"]

    task = {
        "dataset": dataset,
        "variables": variables,
        "data_path": data_path,

        "output_directory": f"{work_dir}/preproc/{dataset['dataset']}/{short_name}",
        "output_data_source_file": "data_source.yml",
    }

    config = {}

    get_data(
        task=task,
        work_dir=work_dir,
        config=config
    )


def main():
    datasets = climwip_recipe.exp_datasets
    variables = climwip_recipe.graph_variables

    tasks = [
        {
            "exp_dataset": d,
            "variable": v
        }
        for d, v in itertools.product(datasets, variables)
    ]

    for task in tasks:
        run(**task)

if __name__ == "__main__":
    main()
