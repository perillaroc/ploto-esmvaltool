from ploto_esmvaltool.plotter.esmvaltool_diag_plotter import run_plotter
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.consecdrydays import generate_default_task

def main():
    work_dir = "./dist/tests/esmvalcore_pre_processor"

    task = generate_default_task()
    task = {
        **task,
        "config": {
            "log_level": "info",
            "write_netcdf": True,
            "write_plots": True,
            "output_file_type": "png",
            "profile_diagnostic": False,
            "auxiliary_data_dir": "/home/hujk/ploto/esmvaltool/cases/case1/case1.2/auxiliary_data"
        },
        "input_files": [
            "{work_dir}/preproc/pr/metadata.yml"
        ],
    }

    config = {
        "esmvaltool": {
            "executables": {
                "py": "/home/hujk/anaconda3/envs/wangdp-esm/bin/python"
            },
            "recipes": {
                "base": "/home/hujk/ploto/esmvaltool/study/esmvaltool/ESMValTool/esmvaltool/recipes",
            },
            "diag_scripts": {
                "base": "/home/hujk/ploto/esmvaltool/study/esmvaltool/ESMValTool/esmvaltool/diag_scripts",
            },
        }
    }

    run_plotter(
        task=task,
        work_dir=work_dir,
        config=config
    )


if __name__ == "__main__":
    main()
