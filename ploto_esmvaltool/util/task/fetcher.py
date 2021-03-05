import typing


def get_fetcher_task(
        diagnostic_name: str,
        variable: typing.Dict,
        config: typing.Dict,
):
    task = {
        "products": [
            {
                "variable": variable,
                "output": {
                    "output_directory": "{alias}/{variable_group}",
                    "output_data_source_file": "data_source.yml",
                }
            }
        ],

        "config": config,

        "output": {
            "output_directory": "{work_dir}" + f"/{diagnostic_name}/fetcher/preproc",
        }
    }
    return task
