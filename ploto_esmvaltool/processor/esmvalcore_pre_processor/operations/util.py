import typing
import warnings

from esmvalcore.preprocessor import (
    DEFAULT_ORDER,
    MULTI_MODEL_FUNCTIONS
)


def _get_settings(
        operation: typing.Dict,
        settings: typing.Union[typing.Dict, bool],
) -> typing.Optional[typing.Union[typing.Dict, bool]]:
    """
    Update settings using operation["settings"].

    Parameters
    ----------
    operation: typing.Dict
    settings: typing.Dict

    Returns
    -------
    typing.Dict:
        Combined settings.
    """
    operation_type = operation["type"]

    new_settings = settings.get(operation_type, {})
    # settings could be True or False or None
    if new_settings is None or isinstance(new_settings, bool):
        return new_settings

    new_settings = new_settings.copy()

    if "settings" not in operation:
        return new_settings

    operation_settings = operation["settings"]
    if operation_type in operation_settings:
        new_settings = {
            **new_settings,
            **operation_settings[operation_type],
        }
    return new_settings


def _get_default_operations() -> typing.List:
    warnings.warn("Please use get_default_settings() and get_operations()", DeprecationWarning)
    return [
        # {
        #     "type": "load",
        # },
        {
            "type": "fix_metadata",
        },
        {
            "type": "concatenate",
        },
        {
            "type": "cmor_check_metadata",
        },
        {
            "type": "clip_start_end_year"
        },
        {
            "type": "fix_data"
        },
        {
            "type": "cmor_check_data"
        },
    ]


def get_default_settings():
    settings = {
        "fix_metadata": {},
        "concatenate": {},
        "cmor_check_metadata": {},
        "clip_start_end_year": {},
        "fix_data": {},
        "cmor_check_data": {},
    }

    return settings


def split_derive_settings(settings, order=DEFAULT_ORDER):
    before = {}
    for step in order:
        if step == "derive":
            break
        if step in settings:
            before[step] = settings[step]
    after = {
        k: v
        for k, v in settings.items() if not (k == "derive" or k in before)
    }

    after["derive"] = True
    after['fix_file'] = False
    after['fix_metadata'] = False
    after['fix_data'] = False
    return before, after


def get_operations(settings, order=DEFAULT_ORDER):
    warnings.warn("Please use get_operation_blocks() function", PendingDeprecationWarning)
    operations = []
    for step in order[order.index("load") + 1: order.index("save")]:
        if step in settings and (settings[step] != False):
            operations.append({
                "type": step,
                "settings": settings[step]
            })

    return operations


def get_operation_blocks(settings, order=DEFAULT_ORDER) -> typing.List:
    blocks = []
    previous_step_type = None
    for step in order[order.index("load") + 1: order.index("save")]:
        if step in settings and (settings[step] != False) and (settings[step] is not None):
            step_type = step in MULTI_MODEL_FUNCTIONS
            if step_type is not previous_step_type:
                block = []
                blocks.append(block)
            previous_step_type = step_type
            block.append({
                "type": step,
                "settings": settings[step]
            })

    return blocks


def is_multi_model_operation(operation):
    return operation["type"] in MULTI_MODEL_FUNCTIONS
