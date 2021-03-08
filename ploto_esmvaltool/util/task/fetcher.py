import typing

from ploto_esmvaltool.util.esmvaltool import get_derive_input_variables


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


def get_fetcher_tasks(
        diagnostic_name,
        variable,
        config,
):
    tasks = []

    if not variable["derive"]:
        tasks.append(get_fetcher_task(
            diagnostic_name=diagnostic_name,
            variable=variable,
            config=config,
        ))
    else:
        input_variables = get_derive_input_variables(
            variable=variable
        )

        for v in input_variables:
            task = get_fetcher_task(
                diagnostic_name=diagnostic_name,
                variable=v,
                config=config
            )

            tasks.append(task)

    return tasks
