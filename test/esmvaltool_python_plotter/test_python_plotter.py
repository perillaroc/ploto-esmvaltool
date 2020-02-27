from ploto_esmvaltool.plotter.esmvaltool_python_plotter import run_plotter


def test():
    run_plotter(
        task={
            "step_type": "plotter",
            "type": "ploto_esmvaltool.plotter.esmvaltool_python_plotter",
            "settings_file_path": "./dist/cases/case1/settings.yml",
            "force": "false",
            "ignore_existing": "false",
            "log_level": "debug",
            "diag_script": {
                "group": "base",
                "name": "examples/diagnostic.py",
            }
        },
        work_dir="./dist/cases/case1/run",
        config={
            "esmvaltool_python_plotter": {
            },
            "esmvaltool": {
                "executables": {
                    "py": "/home/hujk/.pyenv/versions/anaconda3-2019.10/envs/esmvaltool/bin/python3"
                },
                "recipes": {
                    "base": "/home/hujk/ploto/esmvaltool/study/esmvaltool/ESMValTool/esmvaltool/recipes",
                },
                "diag_scripts": {
                    "base": "/home/hujk/ploto/esmvaltool/study/esmvaltool/ESMValTool/esmvaltool/diag_scripts",
                },
            }
        },
    )


if __name__ == "__main__":
    test()
