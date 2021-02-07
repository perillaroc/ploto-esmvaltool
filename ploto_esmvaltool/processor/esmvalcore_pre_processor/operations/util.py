import typing


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
        {
            "type": "load",
        },
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
