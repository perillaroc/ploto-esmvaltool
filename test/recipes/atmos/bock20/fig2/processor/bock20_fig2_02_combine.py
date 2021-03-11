from pathlib import Path

from ploto_esmvaltool.processor.esmvaltool_util_processor import run_processor
from ploto_esmvaltool.util.esmvaltool import (
    get_datasets,
)
from ploto_esmvaltool.util.task import (
    get_combine_metadata_task
)
from test.recipes.atmos.bock20 import (
    recipe as bock20_recipe,
    config as bock20_config,
)


diagnostic_name = "fig_2"


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
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case108/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    # recipe
    variables = bock20_recipe.fig2.variables
    variable_additional_datasets = bock20_recipe.fig2.variable_additional_datasets
    additional_datasets = bock20_recipe.fig2.additional_datasets

    # get all datasets
    datasets = get_datasets(
        variables=variables,
        variable_additional_datasets=variable_additional_datasets,
        additional_datasets=additional_datasets
    )

    processor_tasks = []
    for variable in variables:
        v_datasets = datasets[variable["variable_group"]]
        preprocessor = variable.get("preprocessor", "default")
        settings = bock20_recipe.processor_settings.get(preprocessor, {})
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
                    "data_path": bock20_config.data_path
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
