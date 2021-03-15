import itertools
import os
from pathlib import Path

from ploto_esmvaltool.plotter.esmvaltool_diag_plotter import run_plotter

from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.stratosphere import generate_default_plot_task

from test.recipes.atmos.stratosphere import (
    recipe as strato_recipe,
    config as strato_config,
)

diagnostic_name = "aa_strato"


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case109/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    variables = strato_recipe.variables

    plot_tasks = [
        generate_default_plot_task(
            diagnostic_name,
            script_name="autoassess_strato_test_1",
            control_model="CAS-ESM2-0",
            exp_model="FGOALS-g3",
            obs_models=["ERA-Interim"],
            additional_metrics=["ERA-Interim"],
        ),
        generate_default_plot_task(
            diagnostic_name,
            script_name="autoassess_strato_test_2",
            control_model="CAS-ESM2-0",
            exp_model="BCC-CSM2-MR",
            obs_models=["ERA-Interim"],
            additional_metrics=["ERA-Interim"],
        )
    ]

    tasks = [
        {
        "step_type": "plotter",
        "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",

        **plot_task,
        "config": strato_config.plot_config,
        "input_files": [
            f"{work_dir}/{diagnostic_name}/processor/preproc/{v['variable_group']}/metadata.yml"
            for v in variables
        ],
        # "step_work_dir": "{work_dir}" + f"/{diagnostic_name}/plotter"
        }
        for plot_task in plot_tasks
        ]

    config = strato_config.config

    os.chdir(work_dir)

    for task in tasks:
        run_plotter(
            task=task,
            work_dir=work_dir,
            config=config,
        )


if __name__ == "__main__":
    main()
