"""
Quantifying progress across different CMIP phases

References
----------
https://docs.esmvaltool.org/en/latest/recipes/recipe_bock20jgr.html
"""
import typing

from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.util import (
    get_default_settings,
    get_operation_blocks
)


def generate_default_operation_blocks(name, settings=None) -> typing.List:
    mapper = {
        "clim_ref": generate_clim_ref_operation_blocks,
        "default": generate_default_blocks,
    }
    return mapper[name](settings)


def generate_default_blocks(settings):
    settings = {
        **get_default_settings(),
    }

    blocks = get_operation_blocks(settings)
    return blocks


def generate_clim_ref_operation_blocks(settings) -> typing.List:
    if settings is None:
        settings = {
            "regrid": {
                "target_grid": "reference_dataset",
                "scheme": "linear"
            },
            "multi_model_statistics": {
                "span": "full",
                "statistics": ["mean"],
                "exclude": ["reference_dataset"]
            }
        }

    settings = {
        **get_default_settings(),
        **settings
    }

    blocks = get_operation_blocks(settings)
    return blocks


def generate_default_plot_task(name=None) -> typing.Dict:
    mapper = {
        "fig_1_cmip6": generate_fig_1_cmip6_plot,
        "fig_2": generate_fig_2_plot,
        "fig_3": generate_fig_3_plot
    }
    return mapper[name]()


def generate_fig_1_cmip6_plot() -> typing.Dict:
    return {
        "diagnostic": {
            "recipe": "recipe_bock20.yml",
            "name": "fig_1_cmip6"
        },

        "input_files": [
        ],

        "diagnostic_script": {
            "path": {
                "group": "base",
                "script": "bock20jgr/tsline.ncl",
            },
            "settings": {
                "script": "tsline_anom",
                "time_avg": "yearly",
                "ts_anomaly": "anom",
                "ref_start": 1850,
                "ref_end": 1900,
                "ref_mask": True,
                "plot_units": "degC",
                "y_min": -0.5,
                "y_max": 1.6,
                "volcanoes": True,
                "write_stat": True,
                "styleset": "CMIP6",
            }
        },
    }

def generate_fig_2_plot() -> typing.Dict:
    return {
        "diagnostic": {
            "recipe": "recipe_bock20.yml",
            "name": "fig_2"
        },

        "input_files": [
        ],

        "diagnostic_script": {
            "path": {
                "group": "base",
                "script": "bock20jgr/tsline_collect.ncl",
            },
            "settings": {
                "script": "tsline_anom",
                "time_avg": "yearly",
                "ts_anomaly": "anom",
                "ref_start": 1850,
                "ref_end": 1900,
                "ref_mask": True,
                "plot_units": "degC",
                "y_min": -0.5,
                "y_max": 1.2,
                "volcanoes": True,
                "write_stat": True,
                "styleset": "CMIP6",
                "ancestors": [
                    "tas",
                    "tasUnc1",
                    "tasUnc2",
                    "fig_1_*/tsline_anom*"
                ],
                "start_year": 1850,
                "end_year": 2017,
                "ref": ["HadCRUT4"],
                "order": [
                    "CMIP6_historical",
                    #            "CMIP5_historical",
                    #            "CMIP3_20c3m"
                ],
                "stat_shading": True,
                "ref_shading": False,
                "ref_stderr": True,
            }
        },
    }


def generate_fig_3_plot() -> typing.Dict:
    return {
        "diagnostic": {
            "recipe": "recipe_bock20.yml",
            "name": "fig_3"
        },

        "input_files": [
        ],

        "diagnostic_script": {
            "path": {
                "group": "base",
                "script": "bock20jgr/model_bias.ncl",
            },
            "settings": {
                "script": "model_bias",
                "projection": "Robinson",
                "timemean": "annualclim"
            }
        },
    }