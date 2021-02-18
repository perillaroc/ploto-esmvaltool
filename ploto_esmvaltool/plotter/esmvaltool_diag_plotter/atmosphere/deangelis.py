#
import typing

from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.util import _get_default_operations


def generate_default_operations(name) -> typing.List:
    mapper = {
        "spatial_mean": generate_spatial_mean_operations
    }
    return mapper[name]()


def generate_spatial_mean_operations() -> typing.List:
    default_operations = _get_default_operations()
    operations = [
        *default_operations,
        {
            "type": "area_statistics",
            "settings": {
                "operator": "mean"
            }
        },
    ]
    return operations
