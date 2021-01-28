"""
Diurnal temperature range

References
----------
https://docs.esmvaltool.org/en/latest/recipes/recipe_diurnal_temperature_index.html
"""
import typing


def generate_default_plot_task() -> typing.Dict:
    task = {
        "diag": {
            "recipe": "recipe_diurnal_temperature_index.yml",
            "name": "diurnal_temperature_indicator"
        },

        "input_files": [
        ],

        "diag_script": {
            "group": "base",
            "script": "magic_bsc/diurnal_temp_index.R",
            "name": "main"
        },
    }

    return task


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
            "type": "mask_landsea",
            "settings": {
                "fx_variables": {
                    "sftlf": [],
                    "sftof": []
                },
                "mask_out": "sea",
            }
        },
        {
            "type": "extract_region",
        }
    ]
    return operations
