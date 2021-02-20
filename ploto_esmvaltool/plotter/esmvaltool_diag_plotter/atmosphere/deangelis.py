"""
Evaluate water vapor short wave radiance absorption schemes of ESMs with the observations.

References
----------
https://docs.esmvaltool.org/en/latest/recipes/recipe_deangelis15nat.html
"""
import typing

from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.util import (
    get_operations,
    get_default_settings,
)


def generate_default_operations(name, settings=None) -> typing.List:
    mapper = {
        "spatial_mean": generate_spatial_mean_operations,
        "tropical_ocean": generate_tropical_ocean_operations,
    }
    return mapper[name](settings)


def generate_spatial_mean_operations(settings=None) -> typing.List:
    if settings is None:
        settings = {
            "area_statistics": {
                "operator": "mean"
            }
        }

    settings = {
        **get_default_settings(),
        **settings
    }

    operations = get_operations(settings)
    return operations


def generate_tropical_ocean_operations(settings=None) -> typing.List:
    if settings is None:
        settings = {
            "mask_landsea": {
                "mask_out": "land",
                "fx_variables": {
                    "sftlf": [],
                    "sftof": []
                },
            },
            "regrid": {
                "target_grid": "2.5x2.5",
                "scheme": "linear"
            },
            "extract_region": {
                "start_latitude": -30,
                "end_latitude": 30,
                "start_longitude": 0,
                "end_longitude": 360,
            }
        }

    settings = {
        **get_default_settings(),
        **settings
    }

    operations = get_operations(settings)
    return operations



def generate_default_plot_task(name) -> typing.Dict:
    mapper = {
        "f1b": generate_plot_task_f1b,
        "f2ext": generate_plot_task_f2ext,
        "f3f4": generate_plot_task_f3f4,
    }

    task = mapper[name]()
    task["step_work_dir"] = "{work_dir}" + f"/{name}/plotter/"
    return task


def generate_plot_task_f1b():
    return {
        "diagnostic": {
            "recipe": "recipe_deangelisf1b.yml",
            "name": "deangelisf1b"
        },

        "input_files": [
        ],

        "diagnostic_script": {
            "path": {
                "group": "base",
                "script": "deangelis15nat/deangelisf1b.py",
            },
            "settings": {
                "script": "deangelisf1b",
            }
        },
    }


def generate_plot_task_f2ext():
    return {
        "diagnostic": {
            "recipe": "recipe_deangelisf2ext.yml",
            "name": "deangelisf2ext"
        },

        "input_files": [
        ],

        "diagnostic_script": {
            "path": {
                "group": "base",
                "script": "deangelis15nat/deangelisf2ext.py",
            },
            "settings": {
                "script": "deangelisf2ext",
            }
        },
    }


def generate_plot_task_f3f4():
    return {
        "diagnostic": {
            "recipe": "recipe_deangelisf3f4.yml",
            "name": "deangelisf3f4"
        },

        "input_files": [
        ],

        "diagnostic_script": {
            "path": {
                "group": "base",
                "script": "deangelis15nat/deangelisf3f4.py",
            },
            "settings": {
                "script": "deangelisf3f4",
            }
        },
    }
