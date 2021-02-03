from pathlib import Path

from ploto_esmvaltool.fetcher.esmvalcore_fetcher import get_data


def run(
        exp,
        short_name,
        start_year,
        end_year
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case105/ploto/fetcher/"
    Path(work_dir).mkdir(parents=True, exist_ok=True)


    dataset = {
        "dataset": "FGOALS-g3",
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

        "output_directory": f"{work_dir}/preproc/{dataset['exp']}/{short_name}",
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
    tasks = [
        {
            "exp": "historical",
            "short_name": "tas",
            "start_year": 1995,
            "end_year": 2015
        }
    ]
    for task in tasks:
        run(**task)

if __name__ == "__main__":
    main()
