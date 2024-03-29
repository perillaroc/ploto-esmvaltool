"""
Blocking metrics and indices, teleconnections and weather regimes (MiLES)

References
----------
https://docs.esmvaltool.org/en/latest/recipes/recipe_miles.html
"""
import typing

from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.util import _get_default_operations


def generate_default_operations() -> typing.List:
    default_operations = _get_default_operations()
    operations = [
        *default_operations,
        {
            "type": "extract_levels",
            "settings": {
                "levels": 50000,
                "scheme": "linear"
            }
        },
        {
            "type": "regrid",
            "settings": {
                "target_grid": "2.5x2.5",
                "lat_offset": False,
                "scheme": "linear_extrapolate"
            }
        },
        {
            "type": "extract_region",
        }
    ]
    return operations


def generate_default_plot_task(name="miles_block") -> typing.Dict:
    mapper = {
        "miles_block": _generate_plot_task_for_block,
        "miles_eof": _generate_plot_task_for_eof,
        "miles_regimes": _generate_plot_task_for_regimes,
    }
    task = mapper[name]()
    task["step_work_dir"] = "{work_dir}" + f"/{name}/plotter/"
    return task


def _generate_plot_task_for_block() -> typing.Dict:
    task = {
        "diagnostic": {
            "recipe": "recipe_miles_block.yml",
            "name": "miles_diagnostics"
        },

        "input_files": [
        ],

        "diagnostic_script": {
            "path": {
                "group": "base",
                "script": "miles/miles_block.R",
            },
            "settings": {
                "script": "miles_block",
                "seasons": "DJF"
            }
        },
    }

    return task


def _generate_plot_task_for_eof() -> typing.Dict:
    task = {
        "diagnostic": {
            "recipe": "recipe_miles_eof.yml",
            "name": "miles_diagnostics"
        },

        "input_files": [
        ],

        "diagnostic_script": {
            "path": {
                "group": "base",
                "script": "miles/miles_eof.R",
            },
            "settings": {
                "script": "miles_eof",
                "seasons": "DJF",
                "teles": "NAO"
            }
        },
    }

    return task


def _generate_plot_task_for_regimes() -> typing.Dict:
    task = {
        "diagnostic": {
            "recipe": "recipe_miles_regimes.yml",
            "name": "miles_diagnostics"
        },

        "input_files": [
        ],

        "diagnostic_script": {
            "path": {
                "group": "base",
                "script": "miles/miles_regimes.R",
            },
            "settings": {
                "script": "miles_regimes",
                "seasons": "DJF",
                "nclusters": 4
            }
        },
    }

    return task