exp_datasets = [
    {
        "dataset": "ERA-Interim",
        "project": "OBS6",
        "type": "reanaly",
        "version": 1,
        "tier": 3,
    },
    {
        "dataset": "CAS-ESM2-0",
        "project": "CMIP6",
        "exp": "historical",
        "ensemble": "r1i1p1f1",
        "grid": "gn",
    }
]

variables = [
    {
        "variable_group": "pr",
        "short_name": "pr",

        "preprocessor": "preprocessor",
        "mip": "Amon",
        "start_year": 2000,
        "end_year": 2005,

        "reference_dataset": "ERA-Interim"
    },
    {
        "variable_group": "tas",
        "short_name": "tas",

        "preprocessor": "preprocessor",
        "mip": "Amon",
        "start_year": 2000,
        "end_year": 2005,

        "reference_dataset": "ERA-Interim"
    },
]


processor_settings = {
    "preprocessor": {
        "regrid": {
            "target_grid": "reference_dataset",
            "scheme": "linear"
        },
    },
}
