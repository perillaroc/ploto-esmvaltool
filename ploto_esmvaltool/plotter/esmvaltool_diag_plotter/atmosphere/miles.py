"""
Blocking metrics and indices, teleconnections and weather regimes (MiLES)

References
----------
https://docs.esmvaltool.org/en/latest/recipes/recipe_miles.html
"""
import typing


def generate_default_preprocessor_operations() -> typing.List:
    operations = [
        {
            "type": "load",
        },
        {
            "type": "fix_metadata",
        },
        {
            "type": "concatenate",
        },
        {
            "type": "cmor_check_metadata",
        },
        {
            "type": "clip_start_end_year"
        },
        {
            "type": "fix_data"
        },
        {
            "type": "cmor_check_data"
        },
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


def generate_default_plot_task(script="miles_block") -> typing.Dict:
    mapper = {
        "miles_block": _generate_plot_task_for_block,
        "miles_eof": _generate_plot_task_for_eof,
        "miles_regimes": _generate_plot_task_for_regimes,
    }
    task = mapper[script]()
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