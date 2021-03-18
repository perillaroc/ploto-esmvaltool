
cmip6_landcover_datasets = [
    {
        "dataset": "HadGEM3-GC31-LL",
        "project": "CMIP6",
        "exp": "historical",
        "ensemble": "r1i1p1f3",
        "grid": "gn"
    },
]


variables = [
    {
        "variable_group": "treeFrac",
        "short_name": "treeFrac",

        "preprocessor": "pp_cmip",
        "mip": "Lmon",
        "exp": "historical",
        "start_year": 2000,
        "end_year": 2004
    },
    {
        "variable_group": "snc",
        "short_name": "snc",

        "preprocessor": "pp_cmip",
        "mip": "LImon",
        "exp": "historical",
        "start_year": 2000,
        "end_year": 2004
    },
    {
        "variable_group": "alb",
        "short_name": "alb",

        "preprocessor": "pp_cmip",
        "mip": "Amon",
        "exp": "historical",
        "start_year": 2000,
        "end_year": 2004,
        "derive": True,
        "force_derivation": False,
    },
    {
        "variable_group": "grassFrac",
        "short_name": "grassFrac",

        "preprocessor": "pp_cmip",
        "mip": "Lmon",
        "exp": "historical",
        "start_year": 2000,
        "end_year": 2004
    },
    {
        "variable_group": "shrubFrac",
        "short_name": "shrubFrac",

        "preprocessor": "pp_cmip",
        "mip": "Lmon",
        "exp": "historical",
        "start_year": 2000,
        "end_year": 2004
    },
]

variable_additional_datasets = {
    "treeFrac": cmip6_landcover_datasets,
    "snc": cmip6_landcover_datasets,
    "alb": cmip6_landcover_datasets,
    "grassFrac": cmip6_landcover_datasets,
    "shrubFrac": cmip6_landcover_datasets
}
