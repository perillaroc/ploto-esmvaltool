from pathlib import Path

from ploto_esmvaltool.fetcher.esmvalcore_fetcher import get_data
from ploto_esmvaltool.util.esmvaltool import (
    get_datasets
)
from ploto_esmvaltool.util.task import (
    get_fetcher_tasks
)

from test.recipes.future.kcs import (
    config as kcs_config,
    recipe as kcs_recipe,
)


diagnostic_name = "local_resampling"


def get_tasks_for_variable(
        datasets,
        work_dir,
):
    diagnostic = {
        "diagnostic": diagnostic_name
    }
    fetcher_tasks = []
    for task in datasets:
        fetcher_tasks.extend(
            get_fetcher_tasks(
                diagnostic,
                task,
                config={
                    "data_path": kcs_config.data_path
                }
            )
        )
    return fetcher_tasks


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/future/case301/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    # recipe
    variable_additional_datasets = kcs_recipe.local_resampling.variable_additional_datasets
    variables = kcs_recipe.local_resampling.variables

    # get all datasets
    datasets = get_datasets(
        variables=variables,
        variable_additional_datasets=variable_additional_datasets
    )

    # generate fetcher tasks
    fetcher_tasks = []
    for variable in variables:
        fetcher_tasks.extend(
            get_tasks_for_variable(
                datasets=datasets[variable["variable_group"]],
                work_dir=work_dir
            )
        )

    # run fetcher tasks
    for task in fetcher_tasks:
        get_data(
            task,
            config={},
            work_dir=work_dir
        )


if __name__ == "__main__":
    main()
