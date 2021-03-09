import typing
import copy

from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.util import (
    get_operation_blocks,
    is_multi_model_operation,
    split_derive_settings,
    get_default_settings,
)
from ploto_esmvaltool.util.esmvaltool import (
    get_derive_input_variables,
    update_variable_settings
)


def get_processor_tasks_for_variable(
        variable,
        datasets,
        settings,
        diagnostic,
        config,
        work_dir,
):
    variables = datasets

    processor_tasks = []
    # get operation blocks
    settings = {
        **get_default_settings(),
        **settings,
    }

    # derive
    if variable.get("derive", False):
        before_settings, after_settings = split_derive_settings(
            settings
        )

        before_settings = {
            **get_default_settings(),
            **before_settings
        }

        after_settings = {
            **get_default_settings(),
            **after_settings,
        }

        for dataset in datasets:
            input_variables = get_derive_input_variables(
                variable=dataset
            )
            processor_tasks.extend(
                get_processor_tasks_for_operation_block(
                    diagnostic=diagnostic,
                    variable=dataset,
                    variables=input_variables,
                    settings=before_settings,
                    config=config
                )
            )

            processor_tasks.extend(get_processor_tasks_for_operation_block(
                diagnostic=diagnostic,
                variable=dataset,
                variables=[dataset],
                settings=after_settings,
                config=config
            ))
    else:
        processor_tasks.extend(
            get_processor_tasks_for_operation_block(
                diagnostic=diagnostic,
                variable=variable,
                variables=variables,
                settings=settings,
                config=config
            )
        )

    return processor_tasks


def get_processor_tasks_for_operation_block(
        diagnostic: typing.Dict,
        variable: typing.Dict,
        variables: typing.List,
        settings: typing.Dict,
        config: typing.Dict,
):
    blocks = get_operation_blocks(
        settings,
    )

    # get processor tasks
    processor_tasks = []
    for block_index, operation_block in enumerate(blocks):
        variable_products = []
        for v in variables:
            variable_settings = copy.deepcopy(settings)
            variable_settings = update_variable_settings(
                variable=v,
                settings=variable_settings,
                variables=variables,
                config=config,
            )

            variable_products.append({
                "variable": v,
                "settings": variable_settings
            })

        if is_multi_model_operation(operation_block[0]):
            processor_tasks.extend(get_multi_model_processor_tasks(
                diagnostic=diagnostic,
                variable_products=variable_products,
                operation_block=operation_block,
                block_index=block_index,
                total_blocks=len(blocks)
            ))
        else:
            for p in variable_products:
                processor_tasks.extend(get_product_processor_tasks(
                    diagnostic=diagnostic,
                    variable_product=p,
                    operation_block=operation_block,
                    block_index=block_index,
                    total_blocks=len(blocks)
                ))

    return processor_tasks


def get_product_processor_tasks(
        diagnostic: typing.Dict,
        variable_product: typing.Dict,
        operation_block: typing.List,
        block_index: int,
        total_blocks: int = -1,
) -> typing.List:
    variable = variable_product["variable"]
    settings = variable_product["settings"]
    processor_tasks = []

    diagnostic_name = diagnostic["diagnostic"]

    input_section = _get_input_section(
        diagnostic,
        variable,
        block_index,
        total_blocks=total_blocks,
    )

    output_section =  _get_output_section(
        diagnostic,
        variable,
        block_index,
        total_blocks=total_blocks,
    )

    if operation_block[0]["type"] == "derive":
        input_section = _get_input_section_for_derive(
            diagnostic,
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
        diagnostic: typing.Dict,
        variable_products: typing.List[typing.Dict],
        operation_block: typing.List,
        block_index: int,
        total_blocks: int = -1,
) -> typing.List:
    processor_tasks = []

    diagnostic_name = diagnostic["diagnostic"]

    for op in operation_block:
        if op["type"] == "multi_model_statistics":
            if block_index < total_blocks - 1:
                output_directory = f"step-{block_index:02}" + "/multi-model-{operator}/{variable_group}"
            else:
                output_directory = "multi-model-{operator}/{variable_group}"
            op["settings"]["output"] = {
                "output_directory": output_directory,
                "output_file": "MultiModel_{operator}_{mip}_{variable_group}_{start_year}-{end_year}.nc",
            }

    def get_product(variable, settings):
        return {
            "variable": variable,
            "input": _get_input_section(
                diagnostic,
                variable,
                block_index,
                total_blocks
            ),
            "output": _get_output_section(
                diagnostic,
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

        "diagnostic": diagnostic,
    }
    processor_tasks.append(task)

    return processor_tasks


def _get_input_section(
        diagnostic: typing.Dict,
        variable: typing.Dict,
        block_index: int,
        total_blocks: int=-1,
) -> typing.Dict:
    diagnostic_name = diagnostic["diagnostic"]
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
        diagnostic: typing.Dict,
        variable: typing.Dict,
        block_index: int,
        total_blocks: int=-1,
) -> typing.Dict:
    diagnostic_name = diagnostic["diagnostic"]
    if block_index > 0:
        return _get_input_section(
            diagnostic,
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
        diagnostic: typing.Dict,
        variable: typing.Dict,
        block_index: int,
        total_blocks: int=-1
) -> typing.Dict:
    if total_blocks == -1 or block_index < total_blocks - 1:
        return {
            "output_directory": f"step-{block_index:02}" + "/{alias}/{variable_group}",
        }
    else:
        return {
            "output_directory": "{alias}/{variable_group}",
        }
