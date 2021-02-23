exp_datasets = [
    {
        "dataset": "BCC-ESM1",
        "grid": "gn"
    },
    {
        "dataset": "CAS-ESM2-0",
        "institute": "CAS",
        "grid": "gn"
    },
    {
        "dataset": "CAMS-CSM1-0",
        "grid": "gn"
    },
    {
        "dataset": "FGOALS-f3-L",
        "grid": "gr"
    },
    {
        "dataset": "FGOALS-g3",
        "grid": "gn"
    },
    {
        "dataset": "NESM3",
        "grid": "gn"
    },
]

variables = [
    {
        "variable_group": "ua",
        "short_name": "ua",

        "preprocessor": "zonal",
        "reference_dataset": "ERA-Interim",

        "project": "CMIP6",
        "mip": "Amon",
        "exp": "historical",
        "ensemble": "r1i1p1f1",
        "start_year": 1995,
        "end_year": 2014
    }
]


variable_additional_datasets = {
    "ua": [
        {
            "dataset": "ERA-Interim",
            "project": "OBS6",
            "type": "reanaly",
            "version": "1",
            "start_year": 1995,
            "end_year": 2014,
            "tier": 3
        }
    ],
}


processor_settings = {
    "zonal": {
        "regrid": {
            "target_grid": "1x1",
            "scheme": "linear"
        },
        "extract_levels": {
            "scheme": "linear",
            "levels": "reference_dataset"   # replace before create operator
        },
        "zonal_statistics": {
            "operator": "mean"
        },
        "mask_fillvalues": {
            "threshold_fraction": 0.95
        }
    },
}
