import itertools
import os

from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.diurnal_temperature_indicator import (
    generate_default_plot_task,
)
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter import run_plotter

from test.recipes.atmos.diurnal_temperature_index import (
    config as diurnal_config,
    recipe as diurnal_recipe,
)


def run_dry_days():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case102/ploto"

    plot_task = generate_default_plot_task()
    task = {
        "step_type": "plotter",
        "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",

        "config": diurnal_config.plot_config,

        **plot_task,
        "input_files": [
            "{work_dir}" + f"/processor/preproc/{v['variable_group']}/metadata.yml"
            for v in diurnal_recipe.variables
        ],
    }

    config = diurnal_config.config

    os.chdir(work_dir)

    run_plotter(
        task=task,
        work_dir=work_dir,
        config=config,
    )


if __name__ == "__main__":
    run_dry_days()
