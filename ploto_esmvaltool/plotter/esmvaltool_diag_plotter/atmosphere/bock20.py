import typing

from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.util import (
    get_default_settings,
    get_operation_blocks
)
from ploto_esmvaltool.fetcher.esmvalcore_fetcher import get_selected_files



def generate_default_operation_blocks(name, settings=None) -> typing.List:
    mapper = {
        "clim_ref": generate_clim_ref_operation_blocks,
    }
    return mapper[name](settings)


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
    return {
        "diagnostic": {
            "recipe": "recipe_bock20.yml",
            "name": "tsline_anom"
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
