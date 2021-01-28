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
