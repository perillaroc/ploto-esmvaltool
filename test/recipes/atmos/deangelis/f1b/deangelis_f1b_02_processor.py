import itertools
import copy
from pathlib import Path

from loguru import logger

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.deangelis import (
    generate_default_operation_blocks
)

from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.util import (
    split_derive_settings,
    get_operation_blocks,
    get_default_settings,
    is_multi_model_operation
)
from ploto_esmvaltool.util.esmvaltool import (
    get_datasets,
    get_derive_input_variables,
    update_variable_settings
)
from ploto_esmvaltool.util.task import (
    get_product_processor_tasks,
    get_multi_model_processor_tasks
)

from test.recipes.atmos.deangelis import (
    config as deangelis_config,
    recipe as deangelis_recipe,
)

from esmvalcore.preprocessor._derive import get_required


diagnostic_name = "f1b"


def get_operation_block_tasks(
        diagnostic_name,
        variable,
        variables,
        settings,
        config,
):
    processor_tasks = []
    blocks = get_operation_blocks(
        settings,
    )

    # get processor tasks
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
                diagnostic_name=diagnostic_name,
                variable_products=variable_products,
                operation_block=operation_block,
                block_index=block_index,
                total_blocks=len(blocks)
            ))
        else:
            for p in variable_products:
                processor_tasks.extend(get_product_processor_tasks(
                    diagnostic_name=diagnostic_name,
                    variable_product=p,
                    operation_block=operation_block,
                    block_index=block_index,
                    total_blocks=len(blocks)
                ))

    return processor_tasks


def get_tasks_for_variable(
        variable,
        datasets,
        config,
        work_dir,
):
    variables = datasets

    processor_tasks = []
    # get operation blocks
    settings = deangelis_recipe.processor_settings[variable["preprocessor"]]
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
                get_operation_block_tasks(
                    diagnostic_name=diagnostic_name,
                    variable=dataset,
                    variables=input_variables,
                    settings=before_settings,
                    config=config
                )
            )

            processor_tasks.extend(get_operation_block_tasks(
                diagnostic_name=diagnostic_name,
                variable=dataset,
                variables=[dataset],
                settings=after_settings,
                config=config
            ))

            # task = {
            #     "products": [
            #         {
            #             "variable": variable,
            #             "input": {
            #                 "input_metadata_files": [
            #                     (
            #                         "{work_dir}"
            #                         f"/{diagnostic_name}/processor/preproc"
            #                         f"/{v['alias']}/{v['variable_group']}/metadata.yml"
            #                     )
            #                     for v in input_variables
            #                 ],
            #             },
            #             "output": {
            #                 "output_directory": "{alias}/{variable_group}"
            #             },
            #             "settings": settings
            #         }
            #     ],
            #
            #     # operations
            #     "operations": after_opeartion,
            #
            #     "diagnostic": {
            #         "diagnostic_name": diagnostic_name
            #     },
            #
            #     "output": {
            #         "output_directory": "{work_dir}" + f"/{diagnostic_name}/processor/preproc",
            #     },
            #
            #     "step_type": "processor",
            #     "type": "ploto_esmvaltool.processor.esmvalcore_pre_processor",
            # }
            #
            # processor_tasks.append(task)

    else:
        processor_tasks.extend(
            get_operation_block_tasks(
                diagnostic_name=diagnostic_name,
                variable=variable,
                variables=variables,
                settings=settings,
                config=config
            )
        )

    return processor_tasks


def get_processor_tasks(
        exp_dataset,
        variable,
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case106/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    processor_tasks = []

    operations = generate_default_operations(name=variable["preprocessor"])

    before_settings, after_settings = split_derive_settings(
        deangelis_recipe.processor_settings[variable["preprocessor"]]
    )

    before_operations = get_operations({
        **get_default_settings(),
        **before_settings,
    })

    after_operations = get_operations({
        **get_default_settings(),
        **after_settings
    })

    settings = deangelis_recipe.processor_settings[variable["preprocessor"]]

    diagnostic = {
        "diagnostic": "deangelisf1b",
    }

    combined_variable = combine_variable(
        dataset=exp_dataset,
        variable=variable,
    )
    add_variable_info(combined_variable)

    if "derive" in combined_variable and combined_variable["derive"]:
        # 需要的变量，来自 ESMValCore
        required_variables = get_required(
            short_name=combined_variable["short_name"],
            project=combined_variable["project"]
        )

        # 输入变量
        input_variables = [{
            **combined_variable,
            **v,
            "variable_group": f"{combined_variable['short_name']}_derive_input_{v['short_name']}",
            "alias": f"{combined_variable['dataset']}-{combined_variable['exp']}",
        } for v in required_variables]

        for v in input_variables:
            add_variable_info(v, override=True)
            task = {
                "products": [
                    {
                        "variable": v,
                        "input": {
                            "input_data_source_file": (
                                "{work_dir}"
                                f"/{diagnostic_name}/fetcher/preproc"
                                "/{alias}/{variable_group}/data_source.yml"
                            ),
                        },
                        "output": {
                            "output_directory": "{alias}/{variable_group}"
                        },
                        "settings": settings
                    }
                ],

                # operations
                "operations": before_operations,

                "diagnostic": diagnostic,

                "output": {
                    "output_directory": "{work_dir}" + f"/{diagnostic_name}/processor/preproc",
                },

                "step_type": "processor",
                "type": "ploto_esmvaltool.processor.esmvalcore_pre_processor",
            }

            processor_tasks.append(task)

        task = {
            "products": [
                {
                    "variable": combined_variable,
                    "input": {
                        "input_metadata_files": [
                            (
                                "{work_dir}"
                                f"/{diagnostic_name}/processor/preproc"
                                f"/{v['alias']}/{v['variable_group']}/metadata.yml"
                            )
                            for v in input_variables
                        ],
                    },
                    "output": {
                        "output_directory": "{alias}/{variable_group}"
                    },
                    "settings": settings
                }
            ],

            # operations
            "operations": after_operations,

            "diagnostic": diagnostic,

            "output": {
                "output_directory": "{work_dir}" + f"/{diagnostic_name}/processor/preproc",
            },

            "step_type": "processor",
            "type": "ploto_esmvaltool.processor.esmvalcore_pre_processor",
        }

        processor_tasks.append(task)
    else:
        task = {
            "products": [
                {
                    "variable": combined_variable,
                    "input": {
                        "input_data_source_file": (
                            "{work_dir}"
                            f"/{diagnostic_name}/fetcher/preproc"
                            "/{alias}/{variable_group}/data_source.yml"
                        ),
                    },
                    "output": {
                        "output_directory": "{alias}/{variable_group}"
                    },
                    "settings": settings
                }
            ],

            # operations
            "operations": operations,

            "diagnostic": diagnostic,

            "output": {
                "output_directory": "{work_dir}" + f"/{diagnostic_name}/processor/preproc",
            },

            "step_type": "processor",
            "type": "ploto_esmvaltool.processor.esmvalcore_pre_processor",
        }

        processor_tasks.append(task)

    return processor_tasks



def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case106/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    exp_datasets = deangelis_recipe.f1b.exp_datasets
    variables = deangelis_recipe.f1b.variables

    # get all datasets
    datasets = get_datasets(
        datasets=exp_datasets,
        variables=variables,
    )

    processor_tasks = []
    for variable in variables:
        processor_tasks.extend(
            get_tasks_for_variable(
                variable=variable,
                datasets=datasets[variable["variable_group"]],
                config={
                    "data_path": deangelis_config.data_path
                },
                work_dir=work_dir,
            )
        )

    for index, task in enumerate(processor_tasks):
        logger.info(index)
        run_processor(
            task,
            config={},
            work_dir=work_dir
        )


if __name__ == "__main__":
    main()
