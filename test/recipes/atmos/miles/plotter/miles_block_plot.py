from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.miles import (
    generate_default_plot_task,
)
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter import run_plotter

import os
from pathlib import Path


def run_miles_block():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case3/ploto/plotter/block"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    plot_task = generate_default_plot_task(name="miles_block")
    plot_task["diagnostic_script"]["settings"]["seasons"] = "DJF"

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
            "/home/hujk/ploto/esmvaltool/cases/case3/ploto/processor/preproc/metadata.yml"
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
    run_miles_block()
