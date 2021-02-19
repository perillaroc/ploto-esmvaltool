exp_datasets = [
    {
        "dataset": "FGOALS-g3",
        "project": "CMIP6",
        "exp": "piControl",
        "start_year": 501,
        "end_year": 550
    },
    {
        "dataset": "FGOALS-g3",
        "project": "CMIP6",
        "exp": "ssp585",
        "start_year": 2090,
        "end_year": 2099
    },
    {
        "dataset": "FGOALS-g3",
        "project": "CMIP6",
        "exp": "abrupt-4xCO2",
        "start_year": 501,
        "end_year": 550
    },
    {
        "dataset": "CAMS-CSM1-0",
        "project": "CMIP6",
        "exp": "piControl",
        "start_year": 3051,
        "end_year": 3100
    },
    {
        "dataset": "CAMS-CSM1-0",
        "project": "CMIP6",
        "exp": "ssp585",
        "start_year": 2090,
        "end_year": 2099
    },
    {
        "dataset": "CAMS-CSM1-0",
        "project": "CMIP6",
        "exp": "abrupt-4xCO2",
        "start_year": 3051,
        "end_year": 3100
    },
]


spatial_mean_variable = {
    "preprocessor": "spatial_mean",

    "project": "CMIP6",
    "ensemble": "r1i1p1f1",
    "mip": "Amon",
    "grid": "gn",
    "frequency": "mon",
}


variables = [
    {
        "short_name": "rlnst",
        "variable_group": "rlnst",

        **spatial_mean_variable,

        "derive": True,
        "force_derivation": False,
    },
    {
        "short_name": "rsnst",
        "variable_group": "rsnst",

        **spatial_mean_variable,

        "derive": True,
        "force_derivation": False,
    },
    {
        "short_name": "lvp",
        "variable_group": "lvp",

        **spatial_mean_variable,

        "derive": True,
        "force_derivation": False,
    },
    {
        "short_name": "hfss",
        "variable_group": "hfss",

        **spatial_mean_variable,

        "derive": False,
        "force_derivation": False,
    },
]


processor_settings = {
    "spatial_mean": {
        "area_statistics": {
            "operator": "mean"
        },

    }
}
