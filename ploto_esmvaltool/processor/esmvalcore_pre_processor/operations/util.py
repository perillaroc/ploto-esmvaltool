import typing

from esmvalcore.preprocessor import DEFAULT_ORDER


def _get_settings(
        operation: typing.Dict,
        task: typing.Dict,
) -> typing.Dict:
    settings = {}
    if "settings" in operation:
        settings = operation["settings"]

    operation_type = operation["type"]
    if operation_type in task["settings"]:
        settings = {
            **settings,
            **task["settings"][operation_type],
        }
    return settings


def _get_default_operations() -> typing.List:
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
        "cmore_check_data": {},
    }

    return settings


def get_operations(settings, order=DEFAULT_ORDER):
    operations = []
    for step in order[order.index("load") + 1: order.index("save")]:
        if step in settings:
            operations.append({
                "type": step,
                "settings": settings[step]
            })

    return operations