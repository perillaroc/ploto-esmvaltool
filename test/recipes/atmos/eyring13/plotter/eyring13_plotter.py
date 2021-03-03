import itertools
import os
from pathlib import Path

from ploto_esmvaltool.plotter.esmvaltool_diag_plotter import run_plotter

from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.eyring13 import generate_default_plot_task

from test.recipes.atmos.eyring13 import (
    config as eyring13_config,
    recipe as eyring13_recipe,
)

diagnostic_name = "fig12"


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case107/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    variables = eyring13_recipe.variables

    plot_task = generate_default_plot_task(diagnostic_name)

    task = {
        "step_type": "plotter",
        "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",

        **plot_task,
        "config": eyring13_config.plot_config,
        "input_files": [
            f"{work_dir}/{diagnostic_name}/processor/preproc/{v['variable_group']}/{v['variable_group']}_info.ncl"
            for v in variables
        ],
        "step_work_dir": "{work_dir}" + f"/{diagnostic_name}/fig12/plotter"
    }

    config = eyring13_config.config

    os.chdir(work_dir)

    run_plotter(
        task=task,
        work_dir=work_dir,
        config=config,
    )


if __name__ == "__main__":
    main()
