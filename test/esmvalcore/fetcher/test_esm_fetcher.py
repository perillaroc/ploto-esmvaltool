from ploto_esmvaltool.fetcher.esmvalcore_cmip6_fetcher import get_data


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case1/ploto/c1"

    dataset = {
        "dataset": "FGOALS-g3",
        "project": "CMIP6",
        "mip": "day",
        "exp": "1pctCO2",
        "ensemble": "r1i1p1f1",
        "grid": "gn",
        "frequency": "day",

        "start_year": 370,
        "end_year": 371,
    }

    variables = {
        "variables": [
            {
                "short_name": "pr",
            }
        ]
    }

    data_path = {
        "data_path": {
            "CMIP6": [
                "/data/brick/b1/CMIP6_DATA/",
                "/data/brick/b0/CMIP6/",
            ]
        }
    }

    task = {
        **dataset,
        **variables,
        **data_path,

        "output_directory": "preproc/pr",
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
