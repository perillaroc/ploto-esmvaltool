"""
Diurnal temperature range

References
----------
https://docs.esmvaltool.org/en/latest/recipes/recipe_diurnal_temperature_index.html
"""
import typing

from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.util import _get_default_operations


def generate_default_plot_task() -> typing.Dict:
    task = {
        "diagnostic": {
            "recipe": "recipe_diurnal_temperature_index.yml",
            "name": "diurnal_temperature_indicator"
        },

        "input_files": [
        ],

        "diagnostic_script": {
            "path": {
                "group": "base",
                "script": "magic_bsc/diurnal_temp_index.R",
            },
            "settings": {
                "script": "main"
            }
        },
    }

    return task


def generate_default_preprocessor_operations() -> typing.List:
    default_operations = _get_default_operations()
    operations = [
        *default_operations,
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
