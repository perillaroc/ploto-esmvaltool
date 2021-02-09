

exp_datasets = [
    {
        "dataset": "FGOALS-g3",
        "type": "exp",
        "project": "CMIP6",
        "mip": "day",
        "frequency": "day",
        "exp": "amip",
        "ensemble": "r1i1p1f1",
        "start_year": 1980,
        "end_year": 1985,
        "grid": "gn"
    },
    {
        "dataset": "FGOALS-g3",
        "type": "exp",
        "project": "CMIP6",
        "mip": "day",
        "frequency": "day",
        "exp": "historical",
        "ensemble": "r1i1p1f1",
        "start_year": 1980,
        "end_year": 1985,
        "grid": "gn"
    },
]


variables = [
    {
        "variable_group": "zg",
        "short_name": "zg",
        "preprocessor": "preproc",
    }
]

processor_settings = {
    "extract_region": {
        "start_longitude": 0,
        "end_longitude": 360,
        "start_latitude": 20,
        "end_latitude": 90,
    },
    "extract_levels": {
        "levels": [85000., 50000., 25000., 5000.],
        "scheme": "nearest"
    },
    "regrid": {
        "target_grid": "3x3",
        "scheme": "area_weighted"
    }
}