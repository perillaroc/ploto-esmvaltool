from pathlib import Path

from ploto_esmvaltool.fetcher.esmvalcore_fetcher import get_data


def run(
        short_name,
        start_year,
        end_year
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case105/ploto/weights/fetcher/"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    dataset = {
        "dataset": "ERA5",
        "project": "native6",
        "type": "reanaly",
        "version": 1,
        "tier": 3,

        "mip": "Amip",
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
        ],
        "OBS6": [
            #"/home/hujk/clusterfs/wangdp/data/obs"
            "/data/brick/b2/OBS/esmvaltool_output/cmorize_obs_20210119_071639"
        ],
        "native6": [
            "/home/hujk/clusterfs/wangdp/data/rawobs"
        ]
    }

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
    tasks = [
        {
            "short_name": v,
            "start_year": 1995,
            "end_year": 2014
        } for v in ["tas", "pr", "psl"]
    ]
    for task in tasks:
        run(**task)

if __name__ == "__main__":
    main()
