import itertools
from pathlib import Path

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor

from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.util import (
    get_default_settings,
    get_operation_blocks,
    MULTI_MODEL_FUNCTIONS
)

from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.eyring13 import generate_default_operation_blocks

from test.recipes.atmos.eyring13 import (
    config as eyring13_config,
    recipe as eyring13_recipe,
)
from test.recipes.atmos.eyring13.util import update_levels


diagnostic_name = "fig12"


def get_processor_tasks(
        exp_dataset,
        variable,
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case107/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    processor_tasks = []

    diag_dataset = {
        "modeling_realm": [
            "atmos"
        ],
    }

    diag = {
        "diagnostic": diagnostic_name,
    }


    combined_variable = {
        **exp_dataset,
        **variable,
    }
    combined_variable["alias"] = f"{combined_variable['dataset']}-{combined_variable['exp']}"


    settings = eyring13_recipe.processor_settings[combined_variable["preprocessor"]]
    settings = {
        **get_default_settings(),
        **settings,
    }

    settings = update_levels(settings, work_dir, {
        "data_path": eyring13_config.data_path
    })

    task = {
        "input_data_source_file":
            "{work_dir}"
            f"/{diagnostic_name}/fetcher/preproc/{combined_variable['alias']}"
            f"/{combined_variable['variable_group']}/data_source.yml",

        # output
        "output_directory":
            "{work_dir}"
            f"/{diagnostic_name}/processor/preproc/{combined_variable['alias']}"
            f"/{combined_variable['variable_group']}",

        # operations
        "operations": operations,
        "dataset": combined_variable,
        "diagnostic_dataset": diag_dataset,
        "variable": combined_variable,
        "diagnostic": diag,
        "settings": settings
    }
    processor_tasks.append(task)

    return processor_tasks


def get_tasks_for_variable(
        variable,
        datasets,
        additional_datasets,
        work_dir,
):
    """
    recipe_dataset_index 仅在单个变量组内计数，各个变量组之间独立
    """
    exp_datasets = [{
        **d,
        "recipe_dataset_index": index
    } for index, d in enumerate(datasets)]
    current_index = len(exp_datasets)

    additional_datasets = [{
        **d,
        "alias": f"{d['dataset']}-{d['project']}",
        "recipe_dataset_index": current_index + index
    } for index, d in enumerate(additional_datasets)]


    # get all tasks
    exp_tasks = [
        {
            **variable,
            **d,
        }
        for d in exp_datasets
    ]
    exp_tasks = [
        {
            **t,
            "alias": f"{t['dataset']}-{t['project']}",
        } for t in exp_tasks
    ]

    additional_tasks = [
        {
            **variable,
            **d,
        }
        for d in additional_datasets
    ]

    tasks = [
        *exp_tasks,
        *additional_tasks,
    ]

    processor_tasks = []

    # get operation blocks
    settings = eyring13_recipe.processor_settings[variable["preprocessor"]]
    settings = {
        **get_default_settings(),
        **settings,
    }
    settings = update_levels(settings, work_dir, {
        "data_path": eyring13_config.data_path
    })

    operation_blocks = generate_default_operation_blocks(
        variable["preprocessor"],
        settings
    )

    # input section
    for block_index, operations in operation_blocks:
        if block_index == 0:
            for task in tasks:
                input_section = {
                    "input_data_source_file":
                        "{work_dir}"
                        f"/{diagnostic_name}/fetcher/preproc/{variable['variable_group']}"
                        f"/{task['alias']}/data_source.yml",
                }
        else:
            if operations[0]["type"] in MULTI_MODEL_FUNCTIONS:
                # check excludes
                # WARNING: HAS BUG when two multi model steps has different excludes.
                current_tasks = tasks
                for step in operations:
                    exclude_items = step["settings"].get("exclude", None)
                    if exclude_items is None:
                        break
                    def replace_datasets(name):
                        if name == "reference_dataset":
                            return variable["reference_dataset"]
                        else:
                            return name
                    exclude_datasets = map(replace_datasets, exclude_items)
                    current_tasks = [
                        t for t in current_tasks if t not in exclude_datasets
                    ]

                input_section = {
                    "input_metadata_files": [
                        (
                            "{work_dir}"
                            f"/{diagnostic_name}/processor/preproc/{variable['variable_group']}"
                            f"/{task['alias']}/block-{block_index}/metadata.yml"
                        ) for task in current_tasks
                    ]
                }
            else:
                for task in tasks:
                    input_section = {
                        "input_metadata_files": [
                            (
                                "{work_dir}"
                                f"/{diagnostic_name}/processor/preproc/{variable['variable_group']}"
                                f"/{task['alias']}/block-{block_index}/metadata.yml"
                            )
                        ]
                    }



    for block_index, operations in operation_blocks:
        if block_index == 0:
            input_section = {
                "input_data_source_file":
                    "{work_dir}"
                    f"/{diagnostic_name}/fetcher/preproc/{combined_variable['alias']}"
                    f"/{combined_variable['variable_group']}/data_source.yml",
            }
            output_section = {
                "output_directory":
                    "{work_dir}"
                    f"/{diagnostic_name}/processor/preproc/{combined_variable['alias']}"
                    f"/{combined_variable['variable_group']}",
            }
        elif block_index == len(operations) - 1:
            input_section = {
                "input_meta_data":
                    "{work_dir}"
                    f"/{diagnostic_name}/fetcher/preproc/{combined_variable['alias']}"
                    f"/{combined_variable['variable_group']}/data_source.yml",
            }
            output_section = {
                "output_directory":
                    "{work_dir}"
                    f"/{diagnostic_name}/processor/preproc/{combined_variable['alias']}"
                    f"/{combined_variable['variable_group']}",
            }
        else:
            pass



    # operations
    for task in tasks:
        processor_tasks.extend(get_processor_tasks(**task))


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case107/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    exp_datasets = eyring13_recipe.exp_datasets
    exp_datasets = [{
        **d,
        "recipe_dataset_index": index
    } for index, d in enumerate(exp_datasets)]
    current_index = len(exp_datasets)

    variables = eyring13_recipe.variables

    # 观测数据
    variable_additional_datasets = eyring13_recipe.variable_additional_datasets
    for variable in variables:
        if variable["variable_group"] in variable_additional_datasets:
            additional_datasets = variable_additional_datasets[variable["variable_group"]]
            variable_additional_datasets[variable["variable_group"]] = [{
                **d,
                "alias": f"{d['dataset']}-{d['project']}",
                "recipe_dataset_index": current_index + index
            } for index, d in enumerate(additional_datasets)]
            current_index += len(additional_datasets)

    processor_tasks = []

    for variable in variables:
        tasks = [
            {
                "exp_dataset": d,
                "variable": variable,
            }
            for d in exp_datasets
        ]

        if variable["variable_group"] in variable_additional_datasets:
            additional_datasets = variable_additional_datasets[variable["variable_group"]]
            tasks.extend([
                {
                    "exp_dataset": {
                        **variable,
                        **d,
                    },
                    "variable": {},
                }
                for d in additional_datasets
            ])

        # operations



        for task in tasks:
            processor_tasks.extend(get_processor_tasks(**task))

    for task in processor_tasks:
        run_processor(
            task,
            config={},
            work_dir=work_dir
        )


if __name__ == "__main__":
    main()
