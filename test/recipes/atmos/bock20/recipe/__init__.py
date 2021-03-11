from . import (
    fig1,
    fig2,
    fig3,
    fig4,
)


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
