from ploto_esmvaltool.plotter.esmvaltool_diag_plotter import run_plotter


def main():
    work_dir = "./dist/tests/esmvalcore_pre_processor"

    task = {
        "config": {
            "log_level": "info",
            "write_netcdf": True,
            "write_plots": True,
            "output_file_type": "png",
            "profile_diagnostic": False,
            "auxiliary_data_dir": "/home/hujk/ploto/esmvaltool/cases/case1/case1.1/auxiliary_data"
        },
        "diag": {
            "dryindex": "cdd",
            "frlim": 5,
            "plim": 1,
            "quickplot": {
                "plot_type": "pcolormesh",
            },
            "recipe": "recipe_consecdrydays.yml",
            "script": "consecutive_dry_days"
        },
        "input_files": [
            "{work_dir}/preproc/pr/metadata.yml"
        ],

        "diag_script": {
            "group": "base",
            "name": "droughtindex/diag_cdd.py",
        },
    }

    config = {
        "esmvaltool_python_plotter": {
        },
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
