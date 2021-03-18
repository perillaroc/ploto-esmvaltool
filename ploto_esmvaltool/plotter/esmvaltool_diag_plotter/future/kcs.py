

import typing
from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.util import (
    get_default_settings,
    get_operation_blocks
)


def generate_default_operation_blocks(name, settings=None) -> typing.List:
    mapper = {
        "preprocessor_global": generate_preprocessor_global_blocks,
        "preprocessor_local": generate_preprocessor_local_blocks,
    }
    return mapper[name](settings)


def generate_default_blocks(settings):
    settings = {
        **get_default_settings(),
    }

    blocks = get_operation_blocks(settings)
    return blocks


def generate_preprocessor_global_blocks(settings) -> typing.List:
    if settings is None:
        settings = {
            "custom_order": True,
            "area_statistics": {
                "operator": "mean"
            },
            "annual_statistics": {
                "operator": "mean",
            },
            "anomalies": {
                "period": "full",
                "reference": {
                    "start_year": 1981,
                    "start_month": 1,
                    "start_day": 1,
                    "end_year": 2010,
                    "end_month": 12,
                    "end_day": 31
                },
                "standardize": False
            },
            "multi_model_statistics": {
                "span": "full",
                "statistics": ["p10", "p90"]
            }
        }

    settings = {
        **get_default_settings(),
        **settings
    }

    blocks = get_operation_blocks(settings)
    return blocks


def generate_preprocessor_local_blocks(settings) -> typing.List:
    if settings is None:
        settings = {
            "extract_point": {
                "longitude": 6.25,
                "latitude": 51.21,
                "scheme": "linear"
            }
        }

    settings = {
        **get_default_settings(),
        **settings
    }

    blocks = get_operation_blocks(settings)
    return blocks


def generate_default_plot_task(name, **kwargs) -> typing.Dict:
    mapper = {
        "global_matching": generate_global_matching_plot,
        "local_resampling": generate_local_resampling_plot,
    }
    return mapper[name](**kwargs)


def generate_global_matching_plot(
        **kwargs
) -> typing.Dict:
    return {
        "diagnostic": {
            "recipe": "recipe_spei.yml",
            "name": "global_matching"
        },

        "input_files": [
        ],

        "diagnostic_script": {
            "path": {
                "group": "base",
                "script": "kcs/global_matching.py",
            },
            "settings": {
                "script": "global_matching",
                "scenario_years": [2050, 2085],
                "scenario_percentiles": ["P10", "P90"]
            }
        }
    }


def generate_local_resampling_plot(
        **kwargs
) -> typing.Dict:
    return {
        "diagnostic": {
            "recipe": "recipe_spei.yml",
            "name": "local_resampling"
        },

        "input_files": [
        ],

        "diagnostic_script": {
            "path": {
                "group": "base",
                "script": "kcs/local_resampling.py",
            },
            "settings": {
                "script": "resample",
                "control_period": [1981, 2010],
                "n_samples": 8,
                "scenarios": {
                    "ML_MOC": {
                        "description": "Moderate warming / low changes in seasonal temperature & precipitation, mid-century",
                        "global_dT": 1.0,
                        "scenario_year": 2050,
                        "resampling_period": [2021, 2050],
                        "dpr_winter": 4,
                        "pr_summer_control": [25, 55],
                        "pr_summer_future": [45, 75],
                        "tas_winter_control": [50, 80],
                        "tas_winter_future": [20, 50],
                        "tas_summer_control": [0, 100],
                        "tas_summer_future": [0, 50],
                    },
                    "ML_EOC": {
                        "description": "Moderate warming / low changes in seasonal temperature & precipitation, mid-century",
                        "global_dT": 1.5,
                        "scenario_year": 2085,
                        "resampling_period": [2031, 2060],
                        "dpr_winter": 6,
                        "pr_summer_control": [10, 40],
                        "pr_summer_future": [60, 90],
                        "tas_winter_control": [50, 80],
                        "tas_winter_future": [20, 50],
                        "tas_summer_control": [0, 100],
                        "tas_summer_future": [0, 50],
                    },
                    "WH_EOC": {
                        "description": "High warming / high changes in seasonal temperature & precipitation, end of century",
                        "global_dT": 3.0,
                        "scenario_year": 2085,
                        "resampling_period": [2066, 2095],
                        "dpr_winter": 24,
                        "pr_summer_control": [60, 100],
                        "pr_summer_future": [0, 40],
                        "tas_winter_control": [20, 50],
                        "tas_winter_future": [50, 80],
                        "tas_summer_control": [10, 50],
                        "tas_summer_future": [60, 100],
                    }
                }
            }
        }
    }