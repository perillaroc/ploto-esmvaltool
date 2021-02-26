from pathlib import Path

from ploto_esmvaltool.processor.esmvaltool_util_processor import run_processor

from test.recipes.atmos.deangelis import (
    config as deangelis_config,
    recipe as deangelis_recipe,
)


diagnostic_name = "f3f4"


def get_combined_task(
        exp_datasets,
        variable,
):
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case106/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    variable_group = variable["variable_group"]
    task = {
        "util_type": "combine_metadata",
        "metadata_files": [
            "{work_dir}" + f"/{diagnostic_name}/processor/preproc/{d['alias']}/{variable_group}/metadata.yml"
            for d in exp_datasets
        ],
        "output_directory": "{work_dir}" + f"/{diagnostic_name}/processor/preproc/{variable_group}"
    }
    return task


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case106/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    exp_datasets = deangelis_recipe.f3f4.exp_datasets
    exp_datasets = [{
        **d,
        "alias": f"{d['dataset']}-{d['exp']}",
    } for d in exp_datasets]
    variables = deangelis_recipe.f3f4.variables

    tasks = []

    # 观测数据
    variable_additional_datasets = deangelis_recipe.f3f4.variable_additional_datasets
    for variable in variables:
        if variable["variable_group"] in variable_additional_datasets:
            additional_datasets = variable_additional_datasets[variable["variable_group"]]
            additional_datasets = [{
                **d,
                "alias": f"{d['dataset']}-{d['project']}",
            } for d in additional_datasets]
            tasks.append({
                "exp_datasets": [
                    *exp_datasets,
                    *additional_datasets,
                ],
                "variable": variable,
            })
        else:
            tasks.append({
                "exp_datasets": exp_datasets,
                "variable": variable,
            })

    processor_tasks = []
    for task in tasks:
        processor_tasks.append(get_combined_task(**task))

    for task in processor_tasks:
        run_processor(
            task,
            config={},
            work_dir=work_dir
        )


if __name__ == "__main__":
    main()
