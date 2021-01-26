import typing

from esmvalcore.preprocessor import mask_landsea

from .util import _get_settings


def run_mask_landsea(
        operation: typing.Dict,
        task: typing.Dict,
        cube,
        **kwargs
):
    settings = _get_settings(operation, task)

    fx_variables = settings["fx_variables"]
    mask_out = settings["mask_out"]
    always_use_ne_mask = settings.get("always_use_ne_mask", False)

    cubes = mask_landsea(
        cube,
        fx_variables=fx_variables,
        mask_out=mask_out,
        always_use_ne_mask=always_use_ne_mask,
    )
    return cubes
