

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
