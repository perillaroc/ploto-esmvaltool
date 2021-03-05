import typing


def get_processor_tasks(
        diagnostic_name: str,
        variable_product: typing.Dict,
        operation_block: typing.List,
        block_index: int,
):
    variable = variable_product["variable"]
    settings = variable_product["settings"]
    processor_tasks = []

    diag = {
        "diagnostic": diagnostic_name,
    }

    combined_variable = variable

    task = {
        "products": [
            {
                "variable": combined_variable,
                "input": _get_input_section(diagnostic_name, block_index, combined_variable),
                "output": _get_output_section(diagnostic_name, block_index, combined_variable),
                "settings": settings,
            }
        ],

        # output
        "output": {
            "output_directory": "{work_dir}" + f"/{diagnostic_name}/processor/preproc"
        },

        # operations
        "operations": operation_block,

        "diagnostic": diag,
    }
    processor_tasks.append(task)

    return processor_tasks


def get_multi_model_processor_tasks(
        diagnostic_name: str,
        variable_products: typing.List[typing.Dict],
        operation_block: typing.List,
        block_index: int,
):
    processor_tasks = []

    diag = {
        "diagnostic": diagnostic_name,
    }

    for op in operation_block:
        if op["type"] == "multi_model_statistics":
            op["settings"]["output"] = {
                "output_directory": f"step-{block_index:02}" + "/multi-model-{operator}/{variable_group}",
                "output_file": "MultiModel_{operator}_{mip}_{variable_group}_{start_year}-{end_year}.nc",
            }

    def get_product(variable, settings):
        return {
            "variable": variable,
            "input": _get_input_section(diagnostic_name, block_index, variable),
            "output": _get_output_section(diagnostic_name, block_index, variable),
            "settings": settings
        }

    task = {
        "products": [
            get_product(**variable) for variable in variable_products
        ],

        # output
        "output": {
            "output_directory": "{work_dir}" + f"/{diagnostic_name}/processor/preproc"
        },

        # operations
        "operations": operation_block,

        "diagnostic": diag,
    }
    processor_tasks.append(task)

    return processor_tasks



def _get_input_section(diagnostic_name, block_index, variable):
    if block_index == 0:
        return {
            "input_data_source_file":
                "{work_dir}"
                f"/{diagnostic_name}/fetcher/preproc/{variable['alias']}"
                f"/{variable['variable_group']}/data_source.yml",
        }
    else:
        return {
            "input_metadata_files": [
                "{work_dir}"
                f"/{diagnostic_name}/processor/preproc/step-{block_index-1:02}/{variable['alias']}"
                f"/{variable['variable_group']}/metadata.yml"
            ]
        }


def _get_output_section(diagnostic_name, block_index, variable):
    return {
        "output_directory": f"step-{block_index:02}" + "/{alias}/{variable_group}",
    }
