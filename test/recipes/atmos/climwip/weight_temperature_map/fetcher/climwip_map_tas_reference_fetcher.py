from pathlib import Path
import itertools

from ploto_esmvaltool.fetcher.esmvalcore_fetcher import get_data


def run(
        dataset,
        exp,
        short_name,
        variable_group,
        start_year,
        end_year
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case105/ploto/map/fetcher/"
    Path(work_dir).mkdir(parents=True, exist_ok=True)


    dataset = {
        "dataset": dataset,
        "project": "CMIP6",
        "mip": "Amon",
        "exp": exp,
        "ensemble": "r1i1p1f1",
        "grid": "gn",
        "frequency": "mon",

        "start_year": start_year,
        "end_year": end_year,
    }

    variables = [
        {
            "short_name": short_name,
            "variable_group": variable_group
        }
    ]

    data_path = {
        "CMIP6": [
            "/home/hujk/clusterfs/wangdp/data/CMIP6"
        ]
    }

    task = {
        "dataset": dataset,
        "variables": variables,
        "data_path": data_path,

        "output_directory": f"{work_dir}/preproc/{dataset['dataset']}/{variable_group}",
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
    variables = ["tas"]
    datasets = ["FGOALS-g3", "CAMS-CSM1-0"]

    tasks = [
        {
            "dataset": d,
            "exp": ["historical", "ssp585"],
            "short_name": v,
            "variable_group": f"{v}_reference",
            "start_year": 1995,
            "end_year": 2014
        }
        for v, d in itertools.product(variables, datasets)
    ]


    for task in tasks:
        run(**task)

if __name__ == "__main__":
    main()
