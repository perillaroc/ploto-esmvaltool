

import typing
from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.util import (
    get_default_settings,
    get_operation_blocks
)


def generate_default_operation_blocks(name, settings=None) -> typing.List:
    mapper = {
        "pp_aa_area": generate_pp_aa_area_operation_blocks,
    }
    return mapper[name](settings)


def generate_default_blocks(settings):
    settings = {
        **get_default_settings(),
    }

    blocks = get_operation_blocks(settings)
    return blocks


def generate_pp_aa_area_operation_blocks(settings) -> typing.List:
    if settings is None:
        settings = {
            "regrid": {
            "target_grid": "ERA-Interim",
            "scheme": "linear"
        },
        "extract_levels": {
            "levels": [100000., 50000., 10000., 7000., 5000., 3000., 1000.],
            "scheme": "linear",
        }
        }

    settings = {
        **get_default_settings(),
        **settings
    }

    blocks = get_operation_blocks(settings)
    return blocks



def generate_default_plot_task(name=None, **kwargs) -> typing.Dict:
    mapper = {
        "aa_strato": generate_aa_strato_plot
    }
    return mapper[name](**kwargs)


def generate_aa_strato_plot(
        script_name,
        control_model,
        exp_model,
        obs_models,
        additional_metrics,
        **kwargs
) -> typing.Dict:
    return {
        "diagnostic": {
            "recipe": "recipe_stratosphere.yml",
            "name": "aa_strato"
        },

        "input_files": [
        ],

        "diagnostic_script": {
            "path": {
                "group": "base",
                "script": "autoassess/autoassess_area_base.py",
            },
            "settings": {
                "script": script_name,
                "area": "stratosphere",
                "control_model": control_model,
                "exp_model": exp_model,
                "obs_models": obs_models,
                "additional_metrics": additional_metrics,
                "start": "1997/12/01",
                "end": "2002/12/01",
            }
        }
    }
