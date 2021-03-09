import typing


def get_combine_metadata_tasks_for_variable(
        variable: typing.Dict,
        datasets: typing.List,
        diagnostic: typing.Dict,
        config: typing.Dict,
        work_dir: str,
):
    tasks = datasets

    processor_tasks = []
    processor_tasks.append(get_combine_metadata_task(
        variables=tasks,
        variable=variable,
        diagnostic=diagnostic
    ))

    return processor_tasks


def get_combine_metadata_task(
        variables: typing.List,
        variable: typing.Dict,
        diagnostic: typing.Dict
) -> typing.Dict:
    diagnostic_name = diagnostic["diagnostic"]
    task = {
        "util_type": "combine_metadata",
        "products": [
            {
                "input": {
                    "input_metadata_files": [
                        "{work_dir}" + f"/{diagnostic_name}/processor/preproc/{d['alias']}/{d['variable_group']}/metadata.yml"
                        for d in variables
                    ],
                },
                "output": {
                    "output_directory": f"{variable['variable_group']}"
                }
            }
        ],
        "output": {
            "output_directory": "{work_dir}" + f"/{diagnostic_name}/processor/preproc",
        }
    }

    return task
