from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.miles import (
    generate_default_plot_task,
)
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter import run_plotter

from test.recipes.atmos.miles import recipe as miles_recipe
from test.recipes.atmos.miles import config as miles_config

import os
from pathlib import Path


def run_miles_block():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case103/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    diagnostic_name = "miles_block"

    plot_task = generate_default_plot_task(name=diagnostic_name)
    plot_task["diagnostic_script"]["settings"]["seasons"] = "DJF"

    task = {
        "step_type": "plotter",
        "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",

        **plot_task,
        "config": miles_config.plot_config,
        "input_files": [
            f"{work_dir}/{diagnostic_name}/processor/preproc/metadata.yml"
        ],
    }

    config = miles_config.config

    os.chdir(work_dir)

    run_plotter(
        task=task,
        work_dir=work_dir,
        config=config,
    )


if __name__ == "__main__":
    run_miles_block()
