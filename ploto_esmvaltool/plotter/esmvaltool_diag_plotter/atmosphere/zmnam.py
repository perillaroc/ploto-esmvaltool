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
                "levels": [85000., 50000., 25000., 5000.],
                "scheme": "nearest"
            }
        },
        {
            "type": "regrid",
            "settings": {
                "target_grid": "3x3",
                "scheme": "area_weighted"
            }
        },
        {
            "type": "extract_region",
            "settings": {
                "start_longitude": 0.,
                "end_longitude": 360.,
                "start_latitude": 20.,
                "end_latitude": 90.,
            }
        }
    ]
    return operations


def generate_default_plot_task() -> typing.Dict:
    task = {
        "diagnostic": {
            "recipe": "recipe_zmnam.yml",
            "name": "zmnam"
        },

        "input_files": [
        ],

        "diagnostic_script": {
            "path": {
                "group": "base",
                "script": "zmnam/zmnam.py",
            },
            "settings": {
                "script": "main",
            }
        },
        "step_work_dir": "{work_dir}/plotter/"
    }
    return task


