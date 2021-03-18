import itertools
import os
from pathlib import Path

from ploto_esmvaltool.plotter.esmvaltool_diag_plotter import run_plotter

from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.future.kcs import generate_default_plot_task

from test.recipes.future.kcs import (
    config as kcs_config,
    recipe as kcs_recipe,
)

diagnostic_name = "global_matching"


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/future/case301/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    variables = kcs_recipe.variables

    plot_tasks = [
        {
            **generate_default_plot_task(
                "global_matching"
            ),
            "input_files": [
                f"{work_dir}/{diagnostic_name}/processor/preproc/{v['variable_group']}/metadata.yml"
                for v in variables
            ],
            "step_work_dir": "{work_dir}" + f"/{diagnostic_name}/plotter",
        },
    ]

    tasks = [
        {
            "step_type": "plotter",
            "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",

            **plot_task,
            "config": kcs_config.plot_config,
        }
        for plot_task in plot_tasks
    ]

    config = kcs_config.config

    os.chdir(work_dir)

    for task in tasks:
        run_plotter(
            task=task,
            work_dir=work_dir,
            config=config,
        )


if __name__ == "__main__":
    main()
