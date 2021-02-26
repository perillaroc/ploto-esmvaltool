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
from ploto_esmvaltool.util.esmvaltool import (
    combine_variable,
    add_variable_info
)

from test.recipes.atmos.deangelis import (
    config as deangelis_config,
    recipe as deangelis_recipe,
)

from esmvalcore.preprocessor._derive import get_required


diagnostic_name = "f2ext"


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

    exp_datasets = deangelis_recipe.f2ext.exp_datasets
    exp_datasets = [{
        **d,
        "alias": f"{d['dataset']}-{d['exp']}",
    } for d in exp_datasets]
    variables = deangelis_recipe.f2ext.variables

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

    for task in processor_tasks:
        run_processor(
            task,
            config={},
            work_dir=work_dir
        )


if __name__ == "__main__":
    main()
