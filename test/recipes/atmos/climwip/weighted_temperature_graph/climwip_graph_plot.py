from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.climwip import (
    generate_weighted_temperature_graph_plot_task
)
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter import run_plotter

from pathlib import Path
import os


def run_dry_days():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case105/ploto/graph/plotter"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    plot_task = generate_weighted_temperature_graph_plot_task()
    task = {
        "step_type": "plotter",
        "type": "ploto_esmvaltool.plotter.esmvaltool_diag_plotter",
        **plot_task,
        "config": {
            "log_level": "info",
            "write_netcdf": True,
            "write_plots": True,
            "output_file_type": "png",
            "profile_diagnostic": False,
            "auxiliary_data_dir": "/home/hujk/ploto/esmvaltool/cases/case1/case1.2/auxiliary_data"
        },
        "input_files": [
            "/home/hujk/ploto/esmvaltool/cases/case105/ploto/weights/plotter/work/",
            # "/home/hujk/ploto/esmvaltool/cases/case105/exp2/esmvaltool_output/recipe_climwip_20210204_040911/work/calculate_weights_climwip/climwip",
            "/home/hujk/ploto/esmvaltool/cases/case105/ploto/graph/processor/preproc/tas/metadata.yml",
            # "/home/hujk/ploto/esmvaltool/cases/case105/exp2/esmvaltool_output/recipe_climwip_20210204_040911/preproc/weighted_temperature_graph/tas/metadata.yml"
        ],
    }

    config = {
        "esmvaltool": {
            "executables": {
                "py": "/home/hujk/anaconda3/envs/wangdp-esm/bin/python",
                "r": "/home/hujk/anaconda3/envs/wangdp-esm/bin/Rscript"
            },
            "recipes": {
                "base": "/home/hujk/ploto/esmvaltool/study/esmvaltool/ESMValTool/esmvaltool/recipes",
            },
            "diag_scripts": {
                "base": "/home/hujk/ploto/esmvaltool/study/esmvaltool/ESMValTool/esmvaltool/diag_scripts",
            },
        },
        "base": {
            "run_base_dir": "/home/hujk/ploto/ploto-esmvaltool/dist/cases/case1/run"
        }
    }

    os.chdir(work_dir)

    run_plotter(
        task=task,
        work_dir=work_dir,
        config=config,
    )


if __name__ == "__main__":
    run_dry_days()