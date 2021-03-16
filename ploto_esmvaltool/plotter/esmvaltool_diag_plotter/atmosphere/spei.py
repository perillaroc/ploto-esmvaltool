

import typing
from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.util import (
    get_default_settings,
    get_operation_blocks
)


def generate_default_operation_blocks(name, settings=None) -> typing.List:
    mapper = {
        "preprocessor": generate_preprocessor_operation_blocks,
    }
    return mapper[name](settings)


def generate_default_blocks(settings):
    settings = {
        **get_default_settings(),
    }

    blocks = get_operation_blocks(settings)
    return blocks


def generate_preprocessor_operation_blocks(settings) -> typing.List:
    if settings is None:
        settings = {
            "regrid": {
                "target_grid": "reference_dataset",
                "scheme": "linear"
            },
        }

    settings = {
        **get_default_settings(),
        **settings
    }

    blocks = get_operation_blocks(settings)
    return blocks



def generate_default_plot_task(name, **kwargs) -> typing.Dict:
    mapper = {
        "spi": generate_spi_plot,
        "spei": generate_spei_plot,
    }
    return mapper[name](**kwargs)


def generate_spi_plot(
        **kwargs
) -> typing.Dict:
    return {
        "diagnostic": {
            "recipe": "recipe_spei.yml",
            "name": "diagnostic"
        },

        "input_files": [
        ],

        "diagnostic_script": {
            "path": {
                "group": "base",
                "script": "droughtindex/diag_spi.R",
            },
            "settings": {
                "script": "spi"
            }
        }
    }

def generate_spei_plot():
    return {
        "diagnostic": {
            "recipe": "recipe_spei.yml",
            "name": "diagnostic"
        },

        "input_files": [
        ],

        "diagnostic_script": {
            "path": {
                "group": "base",
                "script": "droughtindex/diag_spei.R",
            },
            "settings": {
                "script": "spei"
            }
        }
    }