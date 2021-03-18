from . import cmip6
from . import obs


processor_settings = {
    "pp_cmip": {
        "custom_order": True,
        "regrid": {
            "target_grid": "2x2",
            "scheme": "linear"
        },
        "extract_month": {
            "month": 7
        },
        "climate_statistics": {
            "operator": "mean"
        },
        "mask_landsea": {
            "mask_out": "sea"
        }
    },
    "pp_obs": {
        "mask_landsea": {
            "mask_out": "sea"
        },
        "extract_month": {
            "month": 7
        },
    }
}
