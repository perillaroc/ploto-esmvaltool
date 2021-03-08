import typing

from ploto_esmvaltool.util.esmvaltool import get_derive_input_variables


def get_product_processor_tasks(
        diagnostic_name: str,
        variable_product: typing.Dict,
        operation_block: typing.List,
        block_index: int,
        total_blocks: int = -1,
):
    variable = variable_product["variable"]
    settings = variable_product["settings"]
    processor_tasks = []

    diagnostic = {
        "diagnostic": diagnostic_name,
    }

    input_section = _get_input_section(
        diagnostic_name,
        variable,
        block_index,
        total_blocks=total_blocks,
    )

    output_section =  _get_output_section(
        diagnostic_name,
        variable,
        block_index,
        total_blocks=total_blocks,
    )

    if operation_block[0]["type"] == "derive":
        input_section = _get_input_section_for_derive(
            diagnostic_name,
            variable,
            block_index,
            total_blocks=total_blocks,
        )

    task = {
        "products": [
            {
                "variable": variable,
                "input": input_section,
                "output": output_section,
                "settings": settings,
            }
        ],
        "output": {
            "output_directory": "{work_dir}" + f"/{diagnostic_name}/processor/preproc"
        },
        "operations": operation_block,
        "diagnostic": diagnostic,
    }
    processor_tasks.append(task)

    return processor_tasks


def get_multi_model_processor_tasks(
        diagnostic_name: str,
        variable_products: typing.List[typing.Dict],
        operation_block: typing.List,
        block_index: int,
        total_blocks: int = -1,
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
            "input": _get_input_section(
                diagnostic_name,
                variable,
                block_index,
                total_blocks
            ),
            "output": _get_output_section(
                diagnostic_name,
                variable,
                block_index,
                total_blocks
            ),
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


def _get_input_section(
        diagnostic_name,
        variable,
        block_index,
        total_blocks=-1,
):
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


def _get_input_section_for_derive(
        diagnostic_name,
        variable,
        block_index,
        total_blocks=-1,
):
    if block_index > 0:
        return _get_input_section(
            diagnostic_name,
            variable,
            block_index,
            total_blocks
        )

    input_variables = get_derive_input_variables(
        variable=variable
    )

    input_section = {
            "input_metadata_files": [
                "{work_dir}"
                f"/{diagnostic_name}/processor/preproc/{v['alias']}"
                f"/{v['variable_group']}/metadata.yml"
                for v in input_variables
            ]
    }

    return input_section


def _get_output_section(
        diagnostic_name,
        variable,
        block_index,
        total_blocks=-1
):
    if total_blocks == -1 or block_index < block_index - 1:
        return {
            "output_directory": f"step-{block_index:02}" + "/{alias}/{variable_group}",
        }
    else:
        return {
            "output_directory": "{alias}/{variable_group}",
        }
