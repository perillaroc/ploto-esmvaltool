from pathlib import Path

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.util.esmvaltool import (
    get_datasets,
)
from ploto_esmvaltool.util.task import (
    get_processor_tasks_for_variable,
)

from test.recipes.atmos.spei import (
    config as spei_config,
    recipe as spei_recipe,
)



diagnostic_name = "diagnostic"


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case110/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    # recipe
    exp_datasets = spei_recipe.exp_datasets
    variables = spei_recipe.variables

    # get all datasets
    datasets = get_datasets(
        datasets=exp_datasets,
        variables=variables,
    )

    processor_tasks = []
    for variable in variables:
        processor_tasks.extend(
            get_processor_tasks_for_variable(
                variable=variable,
                datasets=datasets[variable["variable_group"]],
                settings=spei_recipe.processor_settings[variable["preprocessor"]],
                diagnostic={
                    "diagnostic": diagnostic_name
                },
                config={
                    "data_path": spei_config.data_path
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
