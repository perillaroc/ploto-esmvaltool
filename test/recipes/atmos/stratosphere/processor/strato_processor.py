from pathlib import Path

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.util.esmvaltool import (
    get_datasets,
)
from ploto_esmvaltool.util.task import (
    get_processor_tasks_for_variable,
)

from test.recipes.atmos.stratosphere import (
    config as strato_config,
    recipe as strato_recipe,
)


diagnostic_name = "aa_strato"


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case109/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    # recipe
    exp_datasets = strato_recipe.exp_datasets
    variables = strato_recipe.variables
    additional_datasets = strato_recipe.additional_datasets

    # get all datasets
    datasets = get_datasets(
        datasets=exp_datasets,
        variables=variables,
        additional_datasets=additional_datasets
    )

    processor_tasks = []
    for variable in variables:
        processor_tasks.extend(
            get_processor_tasks_for_variable(
                variable=variable,
                datasets=datasets[variable["variable_group"]],
                settings=strato_recipe.processor_settings[variable["preprocessor"]],
                diagnostic={
                    "diagnostic": diagnostic_name
                },
                config={
                    "data_path": strato_config.data_path
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
