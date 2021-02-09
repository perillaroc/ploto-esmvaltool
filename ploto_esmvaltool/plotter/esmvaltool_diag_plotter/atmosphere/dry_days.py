"""
Consecutive dry days

References
----------
https://docs.esmvaltool.org/en/latest/recipes/recipe_consecdrydays.html
"""
import typing

from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.util import _get_default_operations


def generate_default_plot_task() -> typing.Dict:
    task = {
        "diagnostic": {
            "dryindex": "cdd",
            "frlim": 5,
            "plim": 1,
            "quickplot": {
                "plot_type": "pcolormesh",
            },
            "recipe": "recipe_consecdrydays.yml",
            "name": "dry_days"
        },

        "input_files": [
            "{work_dir}/preproc/pr/metadata.yml"
        ],

        "diagnostic_script": {
            "path": {
                "group": "base",
                "script": "droughtindex/diag_cdd.py",
            },
            "settings": {
                "script": "consecutive_dry_days",
            }
        },

        "step_work_dir": "{work_dir}/plotter/"
    }

    return task


def generate_default_operations() -> typing.List:
    default_operations = _get_default_operations()
    operations = [
        *default_operations
    ]
    return operations
