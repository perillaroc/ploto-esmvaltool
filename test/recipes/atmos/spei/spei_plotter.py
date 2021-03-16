import itertools
import os
from pathlib import Path

from ploto_esmvaltool.plotter.esmvaltool_diag_plotter import run_plotter

from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.spei import generate_default_plot_task

from test.recipes.atmos.spei import (
    config as spei_config,
    recipe as spei_recipe,
)

diagnostic_name = "diagnostic"


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case110/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    variables = spei_recipe.variables

    plot_tasks = [
        {
            **generate_default_plot_task(
                "spi"
            ),
            "input_files": [
                f"{work_dir}/{diagnostic_name}/processor/preproc/pr/metadata.yml"
            ],
            "step_work_dir": "{work_dir}" + f"/{diagnostic_name}/plotter/spi",
        },
        {
            **generate_default_plot_task(
                "spei"
            ),
            "input_files": [
                f"{work_dir}/{diagnostic_name}/processor/preproc/{v['variable_group']}/metadata.yml"
                for v in variables
            ],
            "step_work_dir": "{work_dir}" + f"/{diagnostic_name}/plotter/spei",
        }
    ]

    tasks = [
        {
            "step_type": "plotter",
            "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",

            **plot_task,
            "config": spei_config.plot_config,
        }
        for plot_task in plot_tasks
    ]

    config = spei_config.config

    os.chdir(work_dir)

    for task in tasks:
        run_plotter(
            task=task,
            work_dir=work_dir,
            config=config,
        )


if __name__ == "__main__":
    main()
