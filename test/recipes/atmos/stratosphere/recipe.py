exp_datasets = [
    {
        "dataset": "BCC-CSM2-MR",
        "project": "CMIP6",
        "mip": "Amon",
        "exp": "amip",
        "ensemble": "r1i1p1f1",
        "start_year": 1992,
        "end_year": 2002,
        "grid": "gn",
    },
    {
        "dataset": "CAS-ESM2-0",
        "project": "CMIP6",
        "mip": "Amon",
        "exp": "amip",
        "ensemble": "r1i1p1f1",
        "start_year": 1992,
        "end_year": 2002,
        "grid": "gn",
    },
    {
        "dataset": "FGOALS-g3",
        "project": "CMIP6",
        "mip": "Amon",
        "exp": "amip",
        "ensemble": "r1i1p1f1",
        "start_year": 1992,
        "end_year": 2002,
        "grid": "gn",
    },
]

variables = [
    {
        "variable_group": "ta",
        "short_name": "ta",

        "preprocessor": "pp_aa_area",
        "mip": "Amon",
    },
    {
        "variable_group": "ua",
        "short_name": "ua",

        "preprocessor": "pp_aa_area",
        "mip": "Amon",
    },
    {
        "variable_group": "hus",
        "short_name": "hus",

        "preprocessor": "pp_aa_area",
        "mip": "Amon",
    },
]


additional_datasets = [
    {
        "dataset": "ERA-Interim",
        "project": "OBS6",
        "type": "reanaly",
        "version": "1",
        "tier": 3,
        "start_year": 2000,
        "end_year": 2002,
    }
]


processor_settings = {
    "pp_aa_area": {
        "regrid": {
            "target_grid": "ERA-Interim",
            "scheme": "linear"
        },
        "extract_levels": {
            "levels": [100000., 50000., 10000., 7000., 5000., 3000., 1000.],
            "scheme": "linear",
        }
    },
}
