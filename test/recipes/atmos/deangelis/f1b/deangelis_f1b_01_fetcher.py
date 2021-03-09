from pathlib import Path

from ploto_esmvaltool.fetcher.esmvalcore_fetcher import get_data
from ploto_esmvaltool.util.esmvaltool import (
    get_datasets,
)
from ploto_esmvaltool.util.task import get_fetcher_tasks

from test.recipes.atmos.deangelis import (
    config as deangelis_config,
    recipe as deangelis_recipe,
)


diagnostic_name = "f1b"


def get_tasks_for_variable(
        datasets,
        config,
        work_dir,
):
    tasks = datasets

    diagnostic = {
        "diagnostic": diagnostic_name
    }

    fetcher_tasks = []
    for task in tasks:
        fetcher_tasks.extend(
            get_fetcher_tasks(
                diagnostic,
                variable=task,
                config=config,
            )
        )
    return fetcher_tasks


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case106/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    exp_datasets = deangelis_recipe.f1b.exp_datasets
    variables = deangelis_recipe.f1b.variables

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
                config={
                    "data_path": deangelis_config.data_path
                },
                work_dir=work_dir
            )
        )

    for task in fetcher_tasks:
        get_data(
            task,
            config={},
            work_dir=work_dir
        )


if __name__ == "__main__":
    main()
