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


def generate_calculate_weights_plot_task() -> typing.Dict:
    task = {
        "diagnostic": {
            "recipe": "recipe_climwip.yml",
            "name": "calculate_weights_climwip"
        },

        "input_files": [
        ],

        "diagnostic_script": {
            "path": {
                "group": "base",
                "script": "weighting/climwip/main.py",
            },
            "settings": {
                "script": "climwip",
                "obs_data": "native6",
                "combine_ensemble_members": True,
                "performance_sigma": 0.5,
                "performance_contributions": {
                    "tas_CLIM": 1,
                    "pr_CLIM": 2,
                    "psl_CLIM": 1,

                },
                "independence_sigma": 0.5,
                "independence_contributions": {
                    "tas_CLIM": .5,
                    "pr_CLIM": .25,
                    "psl_CLIM": 0,  # equivalent to not setting it
                }
            }
        },
    }

    return task


def generate_temperature_anomalies_operations(settings: typing.Dict = None) -> typing.List:
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
            "type": "fix_data",
        },
        {
            "type": "cmor_check_data"
        },
        {
            "type": "area_statistics",
            "settings": {
                "operator": "mean"
            }
        },
        {
            "type": "annual_statistics",
            "settings": {
                "operator": "mean"
            }
        },
        {
            "type": "anomalies",
            "settings": {
                "period": "full",
                "standardize": False,
                "reference": {
                    "start_year": 1981,
                    "start_month": 1,
                    "start_day": 1,
                    "end_year": 2010,
                    "end_month": 12,
                    "end_day": 31,
                }
            }
        }
    ]
    return operations


def generate_weighted_temperature_graph_plot_task() -> typing.Dict:
    task = {
        "diagnostic": {
            "recipe": "recipe_climwip.yml",
            "name": "climwip"
        },

        "input_files": [
        ],

        "diagnostic_script": {
            "path": {
                "group": "base",
                "script": "weighting/weighted_temperature_graph.py",
            },
            "settings": {
                "script": "weighted_temperature_graph",
                "weights": "weights.nc"
            }
        },
    }

    return task