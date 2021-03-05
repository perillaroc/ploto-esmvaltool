"""
Ozone and associated climate impacts

References
----------
https://docs.esmvaltool.org/en/latest/recipes/recipe_eyring13jgr.html
"""
import typing

from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.util import (
    get_default_settings,
    get_operation_blocks
)


def generate_default_operation_blocks(name, settings=None) -> typing.List:
    mapper = {
        "zonal": generate_zonal_operation_blocks,
    }
    return mapper[name](settings)


def generate_zonal_operation_blocks(settings=None) -> typing.List:
    if settings is None:
        settings = {
            "regrid": {
                "target_grid": "1x1",
                "scheme": "linear"
            },
            "extract_levels": {
                "scheme": "linear",
                "levels": "reference_dataset"   # replace before create operator
            },
            "zonal_statistics": {
                "operator": "mean"
            },
            "mask_fillvalues": {
                "threshold_fraction": 0.95
            }
        }

    settings = {
        **get_default_settings(),
        **settings
    }

    blocks = get_operation_blocks(settings)
    return blocks


def generate_default_plot_task(name=None) -> typing.Dict:
    return {
        "diagnostic": {
            "recipe": "recipe_eyring13jgr.yml",
            "name": "eyring13jgr_fig12"
        },

        "input_files": [
        ],

        "diagnostic_script": {
            "path": {
                "group": "base",
                "script": "eyring13jgr/eyring13jgr_fig12.ncl",
            },
            "settings": {
                "script": "eyring13jgr_fig12",
                "e13fig12_exp_MMM": "historical",
                "e13fig12_season": "DJF",
                "e13fig12_multimean": True,
            }
        },
    }
