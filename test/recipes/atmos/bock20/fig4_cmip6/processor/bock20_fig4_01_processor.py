from pathlib import Path

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.util.esmvaltool import (
    get_datasets,
)
from ploto_esmvaltool.util.task import (
    get_processor_tasks_for_variable,
)

from test.recipes.atmos.bock20 import (
    config as bock20_config,
    recipe as bock20_recipe,
)


diagnostic_name = "fig_4_cmip6"


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case108/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    # recipe
    variables = bock20_recipe.fig4.variables
    variable_additional_datasets = bock20_recipe.fig4.variable_additional_datasets
    additional_datasets = bock20_recipe.fig4.additional_datasets

    # get all datasets
    datasets = get_datasets(
        variables=variables,
        variable_additional_datasets=variable_additional_datasets,
        additional_datasets=additional_datasets
    )

    processor_tasks = []
    for variable in variables:
        preprocessor = variable.get("preprocessor", "default")
        settings = bock20_recipe.processor_settings.get(preprocessor, {})
        processor_tasks.extend(
            get_processor_tasks_for_variable(
                variable=variable,
                datasets=datasets[variable["variable_group"]],
                settings=settings,
                diagnostic={
                    "diagnostic": diagnostic_name
                },
                config={
                    "data_path": bock20_config.data_path
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
