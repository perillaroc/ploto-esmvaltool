import itertools
import os
from pathlib import Path

from ploto_esmvaltool.plotter.esmvaltool_diag_plotter import run_plotter

from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.land.landcover import generate_default_plot_task

from test.recipes.land.landcover import (
    config as landcover_config,
    recipe as landcover_recipe,
)

diagnostic_name = "obs"


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/land/case401/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    variables = landcover_recipe.obs.variables

    plot_tasks = [
        {
            **generate_default_plot_task(
                diagnostic_name
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
            "config": landcover_config.plot_config,
        }
        for plot_task in plot_tasks
    ]

    config = landcover_config.config

    os.chdir(work_dir)

    for task in tasks:
        run_plotter(
            task=task,
            work_dir=work_dir,
            config=config,
        )


if __name__ == "__main__":
    main()
