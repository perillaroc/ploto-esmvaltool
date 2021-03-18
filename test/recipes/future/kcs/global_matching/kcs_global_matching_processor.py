from pathlib import Path

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.util.esmvaltool import (
    get_datasets,
)
from ploto_esmvaltool.util.task import (
    get_processor_tasks_for_variable,
)

from test.recipes.future.kcs import (
    config as kcs_config,
    recipe as kcs_recipe,
)


diagnostic_name = "global_matching"


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/future/case301/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    # recipe
    variable_additional_datasets = kcs_recipe.variable_additional_datasets
    variables = kcs_recipe.variables

    # get all datasets
    datasets = get_datasets(
        variables=variables,
        variable_additional_datasets=variable_additional_datasets
    )

    processor_tasks = []
    for variable in variables:
        processor_tasks.extend(
            get_processor_tasks_for_variable(
                variable=variable,
                datasets=datasets[variable["variable_group"]],
                settings=kcs_recipe.processor_settings[variable["preprocessor"]],
                diagnostic={
                    "diagnostic": diagnostic_name
                },
                config={
                    "data_path": kcs_config.data_path
                },
                work_dir=work_dir
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
