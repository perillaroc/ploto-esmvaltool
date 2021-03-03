exp_datasets = [
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

        "start_year": 1995,
        "end_year": 2014
    }
]


variable_additional_datasets = {
    "tas": [
        {
            "dataset": "HadCRUT4",
            "project": "OBS",
            "type": "ground",
            "version": "1",
            "tier": 2,
            "end_year": 2017,
        }
    ],
}


processor_settings = {
    "clim_ref": {
        "regrid": {
            "target_grid": "reference_dataset",
            "scheme": "linear"
        },
        "multi_model_statistics": {
            "span": "full",
            "statistics": ["mean"],
            "exclude": ["reference_dataset"]
        }
    },
    "clim": {
        "regrid": {
            "target_grid": "2x2",
            "scheme": "linear"
        },
        "multi_model_statistics": {
            "span": "overlap",
            "statistics": ["mean"],
            "exclude": ["reference_dataset"]
        }
    },
}
