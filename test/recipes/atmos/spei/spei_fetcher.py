from pathlib import Path

from ploto_esmvaltool.fetcher.esmvalcore_fetcher import get_data
from ploto_esmvaltool.util.esmvaltool import (
    get_datasets
)
from ploto_esmvaltool.util.task import (
    get_fetcher_tasks
)

from test.recipes.atmos.spei import (
    config as spei_config,
    recipe as spei_recipe,
)


diagnostic_name = "diagnostic"


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
                    "data_path": spei_config.data_path
                }
            )
        )
    return fetcher_tasks


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
