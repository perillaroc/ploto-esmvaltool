

exp_datasets = [
    {
        "dataset": "FGOALS-g3",
        "type": "exp",
        "project": "CMIP6",
        "mip": "day",
        "frequency": "day",
        "exp": "historical",
        "ensemble": "r1i1p1f1",
        "start_year": 1961,
        "end_year": 1990,
        "grid": "gn"
    },
    {
        "dataset": "FGOALS-g3",
        "type": "exp",
        "project": "CMIP6",
        "mip": "day",
        "frequency": "day",
        "exp": "ssp119",
        "ensemble": "r1i1p1f1",
        "start_year": 2030,
        "end_year": 2080,
        "grid": "gn"
    },
]


variables = [
    {
        "variable_group": "tasmax",
        "short_name": "tasmax",
        "preprocessor": "preproc",
    },
    {
        "variable_group": "tasmin",
        "short_name": "tasmin",
        "preprocessor": "preproc",
    }
]

processor_settings = {
    "preproc": {
        "extract_region": {
            "start_longitude": 70,
            "end_longitude": 140,
            "start_latitude": 15,
            "end_latitude": 55,
        },
        "mask_landsea": {
            "mask_out": "sea"
        },

    }
}