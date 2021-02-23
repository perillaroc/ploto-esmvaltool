import typing

from esmvalcore.preprocessor import (
    mask_landsea,
    mask_fillvalues,
)

from .util import _get_settings


def run_mask_landsea(
        operation: typing.Dict,
        task: typing.Dict,
        cube,
        **kwargs
):
    settings = _get_settings(operation, task)

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
        operation: typing.Dict,
        task: typing.Dict,
        cube,
        **kwargs
):
    settings = _get_settings(operation, task)
    threshold_fraction = settings["threshold_fraction"]
    min_value = settings.get("min_value", None)
    time_window = settings.get("time_window", 1)

    cubes = mask_fillvalues(
        cube,
        threshold_fraction=threshold_fraction,
        min_value=min_value,
        time_window=time_window
    )
    return cubes
