variables = [
    {
        "variable_group": "albDiffiTr13",
        "short_name": "albDiffiTr13",

        "preprocessor": "pp_obs",
        "mip": "Amon"
    },
]

variable_additional_datasets = {
    "albDiffiTr13": [
        {
            "dataset": "Duveiller2018",
            "project": "OBS",
            "tier": 2,
            "version": "v2018",
            "start_year": 2010,
            "end_year": 2010,
            "frequency": "mon",
            "type": "clim",
        }
    ]
}