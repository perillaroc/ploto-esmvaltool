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
    }

    )

    after_operations = get_operations({
        **get_default_settings(),
        **after_settings
    })

    settings = deangelis_recipe.processor_settings[variable["preprocessor"]]

    diag_dataset = {
        "modeling_realm": [
            "atmos"
        ],
    }

    diag = {
        "diagnostic": "deangelisf1b",
    }


    combined_variable = {
        **exp_dataset,
        **variable,
    }

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
            task = {
                "input_data_source_file": "{work_dir}" + f"/fetcher/preproc/{v['alias']}/{v['variable_group']}/data_source.yml",
                # output
                "output_directory": "{work_dir}" + f"/processor/preproc/{v['alias']}/{v['variable_group']}",

                # operations
                "operations": before_operations,

                "dataset": v,
                "diagnostic_dataset": diag_dataset,
                "variable": v,
                "diagnostic": diag,
                "settings": settings
            }
            processor_tasks.append(task)
    else:
        task = {
            "input_data_source_file": "{work_dir}" + f"/fetcher/preproc/{combined_variable['alias']}/{combined_variable['variable_group']}/data_source.yml",
            # output
            "output_directory": "{work_dir}" + f"/processor/preproc/{combined_variable['alias']}/{combined_variable['variable_group']}",

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

    exp_datasets = deangelis_recipe.exp_datasets
    exp_datasets = [{
        **d,
        "alias": f"{d['dataset']}-{d['exp']}",
    } for d in exp_datasets]
    variables = deangelis_recipe.variables

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
