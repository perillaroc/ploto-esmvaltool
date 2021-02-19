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
