import typing

from ploto_esmvaltool.processor.esmvalcore_pre_processor.operations.util import (
    get_default_settings,
    get_operation_blocks
)


def generate_default_operation_blocks(name, settings=None) -> typing.List:
    mapper = {
        "zonal": generate_zonal_operation_blocks,
    }
    return mapper[name](settings)


def generate_zonal_operation_blocks(settings=None) -> typing.List:
    if settings is None:
        settings = {
            "regrid": {
                "target_grid": "1x1",
                "scheme": "linear"
            },
            "extract_levels": {
                "scheme": "linear",
                "levels": "reference_dataset"   # replace before create operator
            },
            "zonal_statistics": {
                "operator": "mean"
            },
            "mask_fillvalues": {
                "threshold_fraction": 0.95
            }
        }

    settings = {
        **get_default_settings(),
        **settings
    }

    blocks = get_operation_blocks(settings)
    return blocks
