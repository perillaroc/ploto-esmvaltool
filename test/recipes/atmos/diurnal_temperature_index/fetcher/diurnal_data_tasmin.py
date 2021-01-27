from ploto_esmvaltool.fetcher.esmvalcore_fetcher import get_data


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case2/ploto/fetcher/"

    dataset = {
        "dataset": "FGOALS-g3",
        "project": "CMIP6",
        "mip": "day",
        "exp": "historical",
        "ensemble": "r1i1p1f1",
        "grid": "gn",
        "frequency": "day",

        "start_year": 1961,
        "end_year": 1962,
    }

    variables = {
        "variables": [
            {
                "short_name": "tasmin",
            }
        ]
    }

    data_path = {
        "data_path": {
            "CMIP6": [
                "/home/hujk/clusterfs/wangdp/data/CMIP6"
            ]
        }
    }

    task = {
        **dataset,
        **variables,
        **data_path,

        "output_directory": f"{work_dir}/preproc/{dataset['exp']}/tasmin",
        "output_data_source_file": "data_source.yml",
    }

    config = {

    }

    get_data(
        task=task,
        work_dir=work_dir,
        config=config
    )

if __name__ == "__main__":
    main()
