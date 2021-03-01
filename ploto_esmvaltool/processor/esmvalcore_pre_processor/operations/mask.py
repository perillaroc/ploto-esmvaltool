import typing

from esmvalcore.preprocessor import (
    mask_landsea,
    mask_fillvalues,
)

from ploto_esmvaltool.processor.esmvalcore_pre_processor._product import Product

from .util import _get_settings


def run_mask_landsea(
        cube,
        settings: typing.Dict,
        **kwargs
):
    fx_variables = getattr(
        settings,
        "fx_variables",
        {
            "sftlf": [],
            "sftof": []
        }
    )
    mask_out = settings["mask_out"]
    always_use_ne_mask = settings.get("always_use_ne_mask", False)

    cubes = mask_landsea(
        cube,
        fx_variables=fx_variables,
        mask_out=mask_out,
        always_use_ne_mask=always_use_ne_mask,
    )
    return cubes


def run_mask_fillvalues(
        products: typing.List[Product],
        threshold_fraction,
        min_value=None,
        time_window=1,
        **kwargs
):

    products = mask_fillvalues(
        products,
        threshold_fraction=threshold_fraction,
        min_value=min_value,
        time_window=time_window
    )
    return products
