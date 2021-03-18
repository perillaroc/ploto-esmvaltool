from . import global_warming
from . import local_resampling


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
