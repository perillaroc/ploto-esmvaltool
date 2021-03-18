from .common import cmip6_datasets, target_datasets


variables = [
    {
        "variable_group": "tas_cmip",
        "short_name": "tas",

        "preprocessor": "preprocessor_global",
    },
    {
        "variable_group": "tas_target",
        "short_name": "tas",

        "preprocessor": "preprocessor_global",
    },
]

variable_additional_datasets = {
    "tas_cmip": cmip6_datasets,
    "tas_target": target_datasets
}
