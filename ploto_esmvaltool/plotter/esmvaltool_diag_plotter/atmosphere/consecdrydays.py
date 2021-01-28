"""
Consecutive dry days

References
----------
https://docs.esmvaltool.org/en/latest/recipes/recipe_consecdrydays.html
"""
import typing


def generate_default_plot_task() -> typing.Dict:
    task = {
        "diag": {
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

        "diag_script": {
            "group": "base",
            "script": "droughtindex/diag_cdd.py",
            "name": "consecutive_dry_days",
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
        }
    ]
    return operations
