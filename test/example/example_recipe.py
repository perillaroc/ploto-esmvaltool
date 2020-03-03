import yaml

from ploto_esmvaltool.processor.esmvaltool_pre_processor.util import generate_variables
from ploto_esmvaltool.plotter.esmvaltool_python_plotter.util import generate_script_settings
from ploto.step import run_steps


def get_processor_tasks(work_dir: str, esmvaltool_config_file: str, raw_recipe: dict):
    # load from config.yml

    config_file = esmvaltool_config_file
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    config["write_ncl_interface"] = False
    config["output"] = work_dir

    # from recipe["documentation"]
    recipe_documentation = raw_recipe["documentation"]

    # from recipe["preprocessors"] + default
    profiles = raw_recipe["preprocessors"]
    if "default" not in profiles:
        profiles["default"] = {}

    # load from recipe["datasets"] + diagnostic's additional datasets from recipe
    # see esmvalcore._recipe.Recipe._initialize_diagnostics
    raw_datasets = [
        {
            'dataset': 'CanESM2',
            'project': 'CMIP5',
            'mip': 'Amon',
            'exp': 'historical',
            'ensemble': 'r1i1p1',
            'start_year': 1996,
            'end_year': 1998,
        },
        {
            'dataset': 'FGOALS-g2',
            'project': 'CMIP5',
            'mip': 'Amon',
            'exp': 'historical',
            'ensemble': 'r1i1p1',
            'start_year': 1996,
            'end_year': 1998,
        }
    ]

    tasks = []
    for variable_group in ["ta", "pr"]:
        # see esmvalcore._recipe.Recipe._initialize_preprocessor_output method.
        raw_variable = {
            # added by esmvalcore.Recipe, values are all from recipe
            "variable_group": variable_group,
            "short_name": variable_group,
            "diagnostic": "diagnostic1",
        }

        if variable_group == "ta":
            raw_variable['preprocessor'] = 'preprocessor1'
        else:
            raw_variable['preprocessor'] = 'default'

        variables = generate_variables(
            raw_recipe=raw_recipe,
            config_file=config_file,
            recipe_file="recipe.yml",
            raw_variable=raw_variable,
            raw_datasets=raw_datasets,
        )

        task = {
            "step_type": "processor",
            "type": "ploto_esmvaltool.processor.esmvaltool_pre_processor",
            "task_name": "diagnostics/ta",
            "variables": variables,
            "profiles": profiles,
            "config": config,
            "recipe_name": "recipe.yml",
            "recipe_documentation": recipe_documentation,
        }
        tasks.append(task)

    return tasks


def get_plotter_task(work_dir: str, esmvaltool_config_file: str, raw_recipe: dict):
    settings = generate_script_settings(
        raw_recipe=raw_recipe,
        config_file=esmvaltool_config_file,
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
    return [task]


def run_example():
    work_dir = "./dist/cases/case1/run"
    esmvaltool_config_file = "./dist/config.yml"

    # load recipe.yml
    recipe_file_path = "./dist/recipe.yml"
    with open(recipe_file_path, "r") as f:
        raw_recipe = yaml.safe_load(f)

    steps = []
    steps.extend(get_processor_tasks(work_dir, esmvaltool_config_file, raw_recipe))
    steps.extend(get_plotter_task(work_dir, esmvaltool_config_file, raw_recipe))

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

    run_steps(steps, work_dir, config)


if __name__ == "__main__":
    run_example()
