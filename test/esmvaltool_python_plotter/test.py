from ploto_esmvaltool.plotter.esmvaltool_python_plotter import run_plotter


def test():
    run_plotter(
        task={
            "step_type": "plotter",
            "type": "ploto_esmvaltool.plotter.esmvaltool_python_plotter",
            "settings_file_path": "./dist/cases/case1/settings.yml",
            "force": "false",
            "ignore_existing": "false",
            "log_level": "debug"
        },
        work_dir="./dist/cases/case1/run",
        config={},
    )


if __name__ == "__main__":
    test()
