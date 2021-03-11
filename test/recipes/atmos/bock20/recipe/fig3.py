variables = [
    {
        "variable_group": "tas",
        "short_name": "tas",

        "preprocessor": "clim",
        "reference_dataset": "ERA5",

        "project": "CMIP6",
        "mip": "Amon",
        "exp": "historical",
        "ensemble": "r1i1p1f1",
        "frequency": "mon",

        "start_year": 1995,
        "end_year": 2014
    },
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
        "dataset": "ERA5",
        "project": "native6",
        "type": "reanaly",
        "version": "1",
        "tier": 3,
    }
]
