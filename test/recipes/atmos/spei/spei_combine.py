from pathlib import Path

from ploto_esmvaltool.processor.esmvaltool_util_processor import run_processor
from ploto_esmvaltool.util.esmvaltool import (
    get_datasets,
)
from ploto_esmvaltool.util.task import (
    get_combine_metadata_task
)
from test.recipes.atmos.spei import (
    config as spei_config,
    recipe as spei_recipe,
)


diagnostic_name = "diagnostic"


def get_tasks_for_variable(
        variable,
        datasets,
        diagnostic,
        config,
        work_dir,
):
    tasks = datasets

    processor_tasks = []
    processor_tasks.append(get_combine_metadata_task(
        variables=tasks,
        variable=variable,
        diagnostic=diagnostic
    ))

    return processor_tasks


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case110/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    exp_datasets = spei_recipe.exp_datasets
    variables = spei_recipe.variables

    datasets = get_datasets(
        datasets=exp_datasets,
        variables=variables,
    )

    processor_tasks = []
    for variable in variables:
        v_datasets = datasets[variable["variable_group"]]
        settings = spei_recipe.processor_settings[variable["preprocessor"]]
        if "multi_model_statistics" in settings:
            statistics = settings["multi_model_statistics"]["statistics"]
            for op in statistics:
                v_datasets.append({
                    "alias": f"multi-model-{op}",
                    "variable_group": variable["variable_group"],
                })

        processor_tasks.extend(
            get_tasks_for_variable(
                variable=variable,
                datasets=v_datasets,
                diagnostic={
                    "diagnostic": diagnostic_name
                },
                config={
                    "data_path": spei_config.data_path
                },
                work_dir=work_dir,
            )
        )

    for task in processor_tasks:
        run_processor(
            task,
            config={},
            work_dir=work_dir
        )


if __name__ == "__main__":
    main()
