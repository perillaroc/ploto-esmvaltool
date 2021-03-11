variables = [
    {
        "variable_group": "tas",
        "short_name": "tas",

        "preprocessor": "clim_ref",
        "reference_dataset": "HadCRUT4",

        "project": "CMIP6",
        "mip": "Amon",
        "exp": "historical",
        "ensemble": "r1i1p1f1",
        "frequency": "mon",

        "start_year": 1850,
        "end_year": 2014
    },
    {
        "variable_group": "tasUnc1",
        "short_name": "tasConf5",
        "mip": "Amon",
        "preprocessor": "default",
    },
    {
        "variable_group": "tasUnc2",
        "short_name": "tasConf95",
        "mip": "Amon",
        "preprocessor": "default",
    }
]


variable_additional_datasets = {
    "tas": [
        {
            "dataset": "BCC-CSM2-MR",
            "grid": "gn",
        },
        {
            "dataset": "BCC-ESM1",
            "grid": "gn",
        },
        # {
        #     "dataset": "CAS-ESM2-0",
        #     "institute": "CAS",
        #     "grid": "gn"
        # },
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
}

additional_datasets = [
    {
        "dataset": "HadCRUT4",
        "project": "OBS",
        "type": "ground",
        "version": "1",
        "tier": 2,
        "end_year": 2017,
    }
]
