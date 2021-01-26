import pathlib

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.diurnal_temperature_indicator import generate_default_preprocessor_operations
from loguru import logger


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case2/ploto/processor"
    operations = generate_default_preprocessor_operations()

    dataset = {
        "dataset": "FGOALS-g3",
        "project": "CMIP6",
        "mip": "day",
        "exp": "historical",
        "ensemble": "r1i1p1f1",
        "grid": "gn",
        "frequency": "day",

        "start_year": 1980,
        "end_year": 1981,
    }

    diag_dataset = {
        "recipe_dataset_index": 0,
        "alias": "historical",
        "modeling_realm": [
            "atmos"
        ],
    }

    variable = {
        "short_name": "tasmax",
        "variable_group": "tasmax",
        "preprocessor": "preproc",
    }

    diag = {
        "diagnostic": "diurnal_temperature_indicator",
    }

    settings = {
        "settings": {
            "extract_region": {
                "start_longitude": 70,
                "end_longitude": 140,
                "start_latitude": 15,
                "end_latitude": 55,
            },
            "mask_landsea": {
                "mask_out": "sea"
            }
        }
    }

    task = {
        # input files
        "input_meta_file": pathlib.Path(pathlib.Path(__file__).parent, "data_source.yml"),
        # output
        "output_directory": "{work_dir}/preproc/historical/tasmax",

        # operations
        "operations": operations,

        **dataset,
        **diag_dataset,
        **variable,
        **diag,
        **settings
    }

    run_processor(
        task=task,
        work_dir=work_dir,
        config={},
    )


if __name__ == "__main__":
    main()
