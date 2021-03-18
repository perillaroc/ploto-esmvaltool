cmip6_datasets = [
    {
        "dataset": "CAMS-CSM1-0",
        "project": "CMIP6",
        "mip": "Amon",
        "exp": ["historical", "ssp585"],
        "ensemble": ["r1i1p1f1", "r2i1p1f1"],
        "start_year": 1961,
        "end_year": 2099,
        "grid": "gn"
    },
    {
        "dataset": "CAS-ESM2-0",
        "project": "CMIP6",
        "mip": "Amon",
        "exp": ["historical", "ssp585"],
        # "ensemble": ["r1i1p1f1", "r3i1p1f1"],
        "ensemble": "r1i1p1f1",
        "start_year": 1961,
        "end_year": 2099,
        "grid": "gn"
    },
    {
        "dataset": "FGOALS-g3",
        "project": "CMIP6",
        "mip": "Amon",
        "exp": ["historical", "ssp585"],
        "ensemble": ["r1i1p1f1", "r2i1p1f1", "r3i1p1f1", "r4i1p1f1"],
        "start_year": 1961,
        "end_year": 2099,
        "grid": "gn"
    }
]

target_datasets = [
    {
        "dataset": "FGOALS-g3",
        "project": "CMIP6",
        "mip": "Amon",
        "exp": ["historical", "ssp585"],
        "ensemble": ["r1i1p1f1", "r2i1p1f1", "r3i1p1f1", "r4i1p1f1"],
        "start_year": 1961,
        "end_year": 2099,
        "grid": "gn"
    }
]

variables = [
    {
        "variable_group": "tas_cmip",
        "short_name": "tas",

        "preprocessor": "preprocessor_global",
    },
    {
        "variable_group": "tas_target",
        "short_name": "tas",

        "preprocessor": "preprocessor_global",
    },
]

variable_additional_datasets = {
    "tas_cmip": cmip6_datasets,
    "tas_target": target_datasets
}

processor_settings = {
    "preprocessor_global": {
        "custom_order": True,
        "area_statistics": {
            "operator": "mean"
        },
        "annual_statistics": {
            "operator": "mean",
        },
        "anomalies": {
            "period": "full",
            "reference": {
                "start_year": 1981,
                "start_month": 1,
                "start_day": 1,
                "end_year": 2010,
                "end_month": 12,
                "end_day": 31
            },
            "standardize": False
        },
        "multi_model_statistics": {
            "span": "full",
            "statistics": ["p10", "p90"]
        }
    },
    "preprocessor_local": {
        "extract_point": {
            "longitude": 6.25,
            "latitude": 51.21,
            "scheme": "linear"
        }
    }
}
