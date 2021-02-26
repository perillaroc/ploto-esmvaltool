from pathlib import Path
import os

from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.climwip import (
    generate_default_plot_task
)
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter import run_plotter

from test.recipes.atmos.climwip import (
    recipe as climwip_recipe,
    config as climwip_config
)

def run_dry_days():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case105/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    variables = climwip_recipe.weights_variables

    plot_task = generate_default_plot_task("calculate_weights_climwip")
    task = {
        "step_type": "plotter",
        "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",
        **plot_task,
        "config": climwip_config.plot_config,
        "input_files": [
            f"/home/hujk/ploto/esmvaltool/cases/case105/ploto/weights/processor/preproc/{variable['variable_group']}/metadata.yml"
            for variable in variables
        ],
    }

    config = climwip_config.config

    os.chdir(work_dir)

    run_plotter(
        task=task,
        work_dir=work_dir,
        config=config,
    )


if __name__ == "__main__":
    run_dry_days()
