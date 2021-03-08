from pathlib import Path
import itertools

from esmvalcore.preprocessor._derive import get_required

from ploto_esmvaltool.fetcher.esmvalcore_fetcher import get_data
from ploto_esmvaltool.util.esmvaltool import (
    get_datasets,
)

from ploto_esmvaltool.util.task import (
    get_fetcher_task
)

from test.recipes.atmos.eyring13 import (
    config as eyring13_config,
    recipe as eyring13_recipe,
)


diagnostic_name = "fig12"


def get_tasks_for_variable(
        datasets,
        work_dir,
):
    tasks = datasets

    fetcher_tasks = []
    for task in tasks:
        fetcher_tasks.append(
            get_fetcher_task(
                diagnostic_name,
                variable=task,
                config={
                    "data_path": eyring13_config.data_path
                }
            )
        )
    return fetcher_tasks


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case107/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    exp_datasets = eyring13_recipe.exp_datasets
    variables = eyring13_recipe.variables
    variable_additional_datasets = eyring13_recipe.variable_additional_datasets

    # get all datasets
    datasets = get_datasets(
        datasets=exp_datasets,
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

    for task in fetcher_tasks:
        get_data(
            task,
            config={},
            work_dir=work_dir
        )


if __name__ == "__main__":
    main()
