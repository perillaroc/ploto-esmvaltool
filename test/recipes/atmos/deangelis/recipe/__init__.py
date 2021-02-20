from . import (
    f1b,
    f2ext,
    f3f4,
)

processor_settings = {
    "spatial_mean": {
        "area_statistics": {
            "operator": "mean"
        },
    },
    "tropical_ocean": {
        "mask_landsea": {
            "mask_out": "land"
        },
        "regrid": {
            "target_grid": "2.5x2.5",
            "scheme": "linear"
        },
        "extract_region": {
            "start_latitude": -30,
            "end_latitude": 30,
            "start_longitude": 0,
            "end_longitude": 360,
        }
    },
    "tropical": {
        "regrid": {
            "target_grid": "2.5x2.5",
            "scheme": "linear"
        },
        "extract_region": {
            "start_latitude": -30,
            "end_latitude": 30,
            "start_longitude": 0,
            "end_longitude": 360,
        }
    }
}
