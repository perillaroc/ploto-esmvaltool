import itertools
from pathlib import Path

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.deangelis import (
    generate_default_operations
)

from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.util import (
    split_derive_settings,
    get_operations,
    get_default_settings,
)

from test.recipes.atmos.deangelis import (
    config as deangelis_config,
    recipe as deangelis_recipe,
)

from esmvalcore.preprocessor._derive import get_required
from esmvalcore._recipe import _add_cmor_info


diagnostic_name = "f3f4"


def get_processor_tasks(
        exp_dataset,
        variable,
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case106/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    processor_tasks = []

    diag_dataset = {
        "modeling_realm": [
            "atmos"
        ],
    }

    diag = {
        "diagnostic": "deangelisf3f4",
    }


    combined_variable = {
        **exp_dataset,
        **variable,
    }

    operations = generate_default_operations(name=combined_variable["preprocessor"])

    before_settings, after_settings = split_derive_settings(
        deangelis_recipe.processor_settings[combined_variable["preprocessor"]]
    )

    before_operations = get_operations({
        **get_default_settings(),
        **before_settings,
    })

    after_operations = get_operations({
        **get_default_settings(),
        **after_settings
    })

    settings = deangelis_recipe.processor_settings[combined_variable["preprocessor"]]

    _add_cmor_info(combined_variable)

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
        } for v in required_variables]

        for v in input_variables:
            task = {
                "input_data_source_file": "{work_dir}" + f"/{diagnostic_name}/fetcher/preproc/{v['alias']}/{v['variable_group']}/data_source.yml",
                # output
                "output_directory": "{work_dir}" + f"/{diagnostic_name}/processor/preproc/{v['alias']}/{v['variable_group']}",

                # operations
                "operations": before_operations,

                "dataset": v,
                "diagnostic_dataset": diag_dataset,
                "variable": v,
                "diagnostic": diag,
                "settings": settings
            }
            processor_tasks.append(task)
        task = {
            "input_metadata_files": [
                "{work_dir}" + f"/{diagnostic_name}/processor/preproc/{v['alias']}/{v['variable_group']}/metadata.yml"
                for v in input_variables
            ],
            # output
            "output_directory": "{work_dir}" + f"/{diagnostic_name}/processor/preproc/{combined_variable['alias']}/{combined_variable['variable_group']}",

            # operations
            "operations": after_operations,

            "dataset": combined_variable,
            "diagnostic_dataset": diag_dataset,
            "variable": combined_variable,
            "diagnostic": diag,
            "settings": settings
        }
        processor_tasks.append(task)
    else:
        task = {
            "input_data_source_file": "{work_dir}" + f"/{diagnostic_name}/fetcher/preproc/{combined_variable['alias']}/{combined_variable['variable_group']}/data_source.yml",
            # output
            "output_directory": "{work_dir}" + f"/{diagnostic_name}/processor/preproc/{combined_variable['alias']}/{combined_variable['variable_group']}",

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


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case106/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    exp_datasets = deangelis_recipe.f3f4.exp_datasets
    exp_datasets = [{
        **d,
        "alias": f"{d['dataset']}-{d['exp']}",
        "recipe_dataset_index": index
    } for index, d in enumerate(exp_datasets)]
    current_index = len(exp_datasets)

    variables = deangelis_recipe.f3f4.variables

    tasks = [
        {
            "exp_dataset": d,
            "variable": v,
        }
        for v, d in itertools.product(variables, exp_datasets)
    ]

    processor_tasks = []
    for task in tasks:
        processor_tasks.extend(get_processor_tasks(**task))

        # 观测数据
        variable_additional_datasets = deangelis_recipe.f3f4.variable_additional_datasets
        for variable in variables:
            if variable["variable_group"] in variable_additional_datasets:
                additional_datasets = variable_additional_datasets[variable["variable_group"]]
                additional_datasets = [{
                    **d,
                    "alias": f"{d['dataset']}-{d['project']}",
                    "recipe_dataset_index": current_index + index
                } for index, d in enumerate(additional_datasets)]
                current_index += len(additional_datasets)
                tasks = [
                    {
                        "exp_dataset": {
                            **variable,
                            **d,
                        },
                        "variable": {},
                    }
                    for d in additional_datasets
                ]
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