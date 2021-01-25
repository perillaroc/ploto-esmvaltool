import yaml

from ploto_esmvaltool.plotter.esmvaltool_python_plotter import run_plotter
from ploto_esmvaltool.plotter.esmvaltool_python_plotter.util import generate_script_settings


def test():
    work_dir = "./dist/cases/case1/run"

    # load recipe.yml
    recipe_file_path = "./dist/recipe.yml"
    with open(recipe_file_path, "r") as f:
        raw_recipe = yaml.safe_load(f)

    config_file = "./dist/config.yml"
    settings = generate_script_settings(
        raw_recipe=raw_recipe,
        config_file=config_file,
        recipe_file="recipe.yml",
        diagnostic_name="diagnostic1",
        script_name="script1",
    )

    task = {
        "step_type": "plotter",
        "type": "ploto_esmvaltool.plotter.esmvaltool_python_plotter",
        "force": "false",
        "ignore_existing": "false",
        "log_level": "debug",
        "diag_script": {
            "group": "base",
            "name": "examples/diagnostic.py",
        },
        "input_files": [
            f"{work_dir}/preproc/diagnostic1/ta/metadata.yml",
            f"{work_dir}/preproc/diagnostic1/pr/metadata.yml",
        ],
        "settings": settings,
    }

    config = {
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
    }

    run_plotter(
        task=task,
        work_dir=work_dir,
        config=config,
    )


if __name__ == "__main__":
    test()
