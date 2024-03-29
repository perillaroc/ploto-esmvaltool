

exp_datasets = [
    {
        "dataset": "FGOALS-g3",
        "type": "exp",
        "project": "CMIP6",
        "mip": "day",
        "exp": "historical",
        "ensemble": "r1i1p1f1",
        "start_year": 1980,
        "end_year": 1981,
        "grid": "gn"
    },
    {
        "dataset": "ERA-Interim",
        "project": "OBS6",
        "type": "reanaly",
        "version": "1",
        "tier": 3,
        "start_year": 1980,
        "end_year": 1981
    }
]


variables = [
    {
        "variable_group": "pr",
        "short_name": "pr",
        "mip": "day",
        "frequency": "day",
        "preprocessor": "preproc1",
    }
]
