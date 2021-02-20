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
        "exp": "abrupt-4xCO2",
        "start_year": 501,
        "end_year": 550
    },
    {
        "dataset": "NESM3",
        "project": "CMIP6",
        "exp": "piControl",
        "start_year": 501,
        "end_year": 550
    },
    {
        "dataset": "NESM3",
        "project": "CMIP6",
        "exp": "abrupt-4xCO2",
        "start_year": 1851,
        "end_year": 1900
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

tropical_variable = {
    "preprocessor": "tropical_ocean",

    "project": "CMIP6",
    "ensemble": "r1i1p1f1",
    "mip": "Amon",
    "grid": "gn",
    "frequency": "mon",
}


variables = [
    {
        "short_name": "rsnstcs",
        "variable_group": "rsnstcs",

        **spatial_mean_variable,

        "derive": True,
        "force_derivation": False,
    },
    {
        "short_name": "rsnstcsnorm",
        "variable_group": "rsnstcsnorm",

        **tropical_variable,

        "derive": True,
        "force_derivation": False,
    },
    {
        "short_name": "tas",
        "variable_group": "tas",

        **spatial_mean_variable,

        "derive": False,
        "force_derivation": False,
    },
    {
        "short_name": "prw",
        "variable_group": "prw",

        **tropical_variable,

        "derive": False,
        "force_derivation": False,
    },
]


variable_additional_datasets = {
    "rsnstcsnorm": [
        {
            "dataset": "CERES-EBAF",
            "project": "obs4mips",
            "type": "satellite",
            "level": "L3B",
            "version": "Ed2-8",
            "start_year": 2001,
            "end_year": 2009,
            "tier": 1
        }
    ],
    "prw": [
        {
            "dataset": "ERA-Interim",
            "project": "OBS6",
            "type": "reanaly",
            "version": 1,
            "start_year": 2003,
            "end_year": 2008,
            "tier": 3
        },
        {
            "dataset": "SSMI-MERIS",
            "project": "obs4mips",
            "type": "satellite",
            "level": "L3",
            "version": "v1-00",
            "start_year": 2003,
            "end_year": 2008,
            "tier": 1
        }
    ]
}