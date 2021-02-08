from pathlib import Path
import itertools

from ploto_esmvaltool.fetcher.esmvalcore_fetcher import get_data

from test.recipes.atmos.climwip.recipe import *


def run(
        exp_dataset,
        variable,
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case105/ploto/weights/fetcher/"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    dataset = {
        **exp_dataset,
        **variable,
    }

    variables = [
        variable
    ]

    data_path = {
        "CMIP6": [
            "/home/hujk/clusterfs/wangdp/data/CMIP6"
        ],
        "OBS6": [
            #"/home/hujk/clusterfs/wangdp/data/obs"
            "/data/brick/b2/OBS/esmvaltool_output/cmorize_obs_20210119_071639"
        ],
        "native6": [
            "/home/hujk/clusterfs/wangdp/data/rawobs"
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

    config = {

    }

    get_data(
        task=task,
        work_dir=work_dir,
        config=config
    )


def main():
    variables = weights_variables
    datasets = obs_datasets

    tasks = [
        {
            "variable": v,
            "exp_dataset": d
        }
        for v, d in itertools.product(variables, datasets)
    ]
    for task in tasks:
        run(**task)


if __name__ == "__main__":
    main()
