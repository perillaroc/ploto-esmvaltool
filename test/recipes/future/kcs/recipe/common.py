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