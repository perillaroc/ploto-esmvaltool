
exp_datasets = [
    {
        "dataset": "FGOALS-g3",
        "project": "CMIP6",
        "exp": ["historical", "ssp585"],
        "ensemble": "r1i1p1f1",
        "grid": "gn",
        "type": "exp"
    },
    {
        "dataset": "CAMS-CSM1-0",
        "project": "CMIP6",
        "exp": ["historical", "ssp585"],
        "ensemble": "r1i1p1f1",
        "grid": "gn",
        "type": "exp"
    }
]

obs_datasets = [
    {
        "dataset": "ERA5",
        "project": "native6",
        "version": "1",
        "tier": 3,
        "type": "reanaly",
    }
]

common_settings = {
    "mip": "Amon",
    "frequency": "mon",
    "start_year": 1995,
    "end_year": 2014,
    "preprocessor": "climatological_mean",
}

weights_variables = [
    {
        "variable_group": "tas_CLIM",
        "short_name": "tas",
        **common_settings
    },
    {
        "variable_group": "pr_CLIM",
        "short_name": "pr",
        **common_settings
    },
    {
        "variable_group": "psl_CLIM",
        "short_name": "psl",
        **common_settings
    },
]


graph_variables = [
    {
        "variable_group": "tas",
        "short_name": "tas",
        "mip": "Amon",
        "frequency": "mon",
        "start_year": 1960,
        "end_year": 2099,
        "preprocessor": "temperature_anomalies",
    }
]

map_settings = {
    "mip": "Amon",
    "frequency": "mon",
    "preprocessor": "climatological_mean",
    "short_name": "tas",
}

map_variables = [
    {
        **map_settings,
        "variable_group": "tas",
        "start_year": 2081,
        "end_year": 2099
    },
    {
        **map_settings,
        "variable_group": "tas_reference",
        "start_year": 1995,
        "end_year": 2014,
    }
]