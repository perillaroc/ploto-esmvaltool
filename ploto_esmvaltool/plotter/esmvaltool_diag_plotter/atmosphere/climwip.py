"""
ClimWIP: independence & performance weighting

References
----------
https://docs.esmvaltool.org/en/latest/recipes/recipe_climwip.html
"""
import typing


def generate_climatological_mean_operations(settings: typing.Dict = None) -> typing.List:
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
            "type": "regrid",
            "settings": {
                "target_grid": "2.5x2.5",
                "scheme": "linear"
            }
        },
        {
            "type": "climate_statistics",
            "settings": {
                "operator": "mean"
            }
        }
    ]
    return operations
