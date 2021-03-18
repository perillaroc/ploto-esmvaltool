from .common import cmip6_datasets, target_datasets

variables = [
    {
        "variable_group": "pr_target",
        "short_name": "pr",

        "preprocessor": "preprocessor_local",
    },
    {
        "variable_group": "tas_target",
        "short_name": "tas",

        "preprocessor": "preprocessor_local",
    },
    {
        "variable_group": "pr_cmip",
        "short_name": "pr",

        "preprocessor": "preprocessor_local",
    },
    {
        "variable_group": "tas_cmip",
        "short_name": "tas",

        "preprocessor": "preprocessor_local",
    },
]

variable_additional_datasets = {
    "pr_target": target_datasets,
    "tas_target": target_datasets,
    "pr_cmip": cmip6_datasets,
    "tas_cmip": cmip6_datasets,
}