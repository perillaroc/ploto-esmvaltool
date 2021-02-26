

exp_datasets = [
    {
        "dataset": "FGOALS-g3",
        "type": "exp",
        "project": "CMIP6",
        "mip": "day",
        "exp": "historical",
        "ensemble": "r1i1p1f1",
        "start_year": 1980,
        "end_year": 1985,
        "grid": "gn"
    },
    {
        "dataset": "ERA-Interim",
        "project": "OBS6",
        "type": "reanaly",
        "version": "1",
        "tier": 3,
        "start_year": 1980,
        "end_year": 1985
    }
]


variables = [
    {
        "variable_group": "zg",
        "short_name": "zg",
        "mip": "day",
        "frequency": "day",
        "preprocessor": "preproc1",
        "reference_dataset": "ERA-Interim"
    }
]

processor_settings = {
    "preproc1": {
        "extract_region": {
            "start_longitude": 0,
            "end_longitude": 360,
            "start_latitude": -1.25,
            "end_latitude": 90,
        },
        "extract_levels": {
            "levels": 50000,
            "scheme": "linear"
        },
        "regrid": {
            "target_grid": "2.5x2.5",
            "scheme": "linear_extrapolate"
        }
    }
}