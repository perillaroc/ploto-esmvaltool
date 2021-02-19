#
import typing

from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.util import (
    get_operations,
    get_default_settings,
)


def generate_default_operations(name, settings=None) -> typing.List:
    mapper = {
        "spatial_mean": generate_spatial_mean_operations
    }
    return mapper[name](settings)


def generate_spatial_mean_operations(settings=None) -> typing.List:
    if settings is None:
        settings = {
            "area_statistics": {
                "operator": "mean"
            }
        }

    settings = {
        **get_default_settings(),
        **settings
    }

    operations = get_operations(settings)
    return operations


def generate_default_plot_task(name) -> typing.Dict:
    mapper = {
        "f1b": generate_plot_task_f1b,
    }

    task = mapper[name]()
    task["step_work_dir"] = "{work_dir}" + f"/{name}/plotter/"
    return task


def generate_plot_task_f1b():
    return {
        "diagnostic": {
            "recipe": "recipe_deangelisf1b.yml",
            "name": "deangelisf1b"
        },

        "input_files": [
        ],

        "diagnostic_script": {
            "path": {
                "group": "base",
                "script": "deangelis15nat/deangelisf1b.py",
            },
            "settings": {
                "script": "deangelisf1b",
            }
        },
    }