def _get_settings(
        operation,
        task,
):
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
