from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.diurnal_temperature_indicator import (
    generate_default_plot_task,
)
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter import run_plotter

import os


def run_dry_days():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case2/ploto/plotter"

    plot_task = generate_default_plot_task()
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
            "/home/hujk/ploto/esmvaltool/cases/case2/ploto/processor/preproc/tasmax/metadata.yml",
            "/home/hujk/ploto/esmvaltool/cases/case2/ploto/processor/preproc/tasmin/metadata.yml"
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
