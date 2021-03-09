from pathlib import Path

from loguru import logger

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.util.esmvaltool import (
    get_datasets,
)
from ploto_esmvaltool.util.task import (
    get_processor_tasks_for_variable
)


from test.recipes.atmos.deangelis import (
    config as deangelis_config,
    recipe as deangelis_recipe,
)


diagnostic_name = "f2ext"


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case106/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    exp_datasets = deangelis_recipe.f2ext.exp_datasets
    variables = deangelis_recipe.f2ext.variables

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
                settings=deangelis_recipe.processor_settings[variable["preprocessor"]],
                diagnostic={
                    "diagnostic": diagnostic_name
                },
                config={
                    "data_path": deangelis_config.data_path
                },
                work_dir=work_dir,
            )
        )

    for index, task in enumerate(processor_tasks):
        logger.info(index)
        run_processor(
            task,
            config={},
            work_dir=work_dir
        )


if __name__ == "__main__":
    main()
