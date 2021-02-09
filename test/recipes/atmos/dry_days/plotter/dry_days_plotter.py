import itertools
import os

from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.dry_days import (
    generate_default_plot_task,
)
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter import run_plotter

from test.recipes.atmos.dry_days import recipe as dry_days_recipe
from test.recipes.atmos.dry_days import config as dry_days_config


def get_plotter():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case101/ploto"

    steps = []

    datasets = dry_days_recipe.exp_datasets
    variables = dry_days_recipe.variables

    plot_task = generate_default_plot_task()
    steps.extend([
        {
            "step_type": "plotter",
            "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",

            **plot_task,
            "config": dry_days_config.plot_config,
            "input_files": [
                "{work_dir}" + f"/processor/preproc/{d['dataset']}/{v['variable_group']}/metadata.yml"
                for d in datasets
            ],
        }
        for v in variables
    ])

    config = dry_days_config.config
    os.chdir(work_dir)

    for task in steps:
        run_plotter(
            task=task,
            work_dir=work_dir,
            config=config,
        )


if __name__ == "__main__":
    get_plotter()
