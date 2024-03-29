import pathlib

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.dry_days import generate_default_operations
from loguru import logger


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case1/ploto/c1"
    operations = generate_default_operations()

    dataset = {
        "dataset": "FGOALS-g3",
        "project": "CMIP6",
        "mip": "day",
        "exp": "1pctCO2",
        "ensemble": "r1i1p1f1",
        "grid": "gn",
        "frequency": "day",

        "start_year": 370,
        "end_year": 371,
    }

    diag_dataset = {
        "recipe_dataset_index": 0,
        "alias": "FGOALS-g3",
        "modeling_realm": [
            "atmos"
        ],
    }

    variable = {
        "short_name": "pr",
        "variable_group": "pr",
        "preprocessor": "default",
    }

    diag = {
        "diagnostic": "dry_days",
    }

    task = {
        # input files
        "input_data_source_file": pathlib.Path(pathlib.Path(__file__).parent, "input_meta_file.yml"),
        # output
        "output_directory": "{work_dir}/preproc/pr",

        # operations
        "operations": operations,

        **dataset,
        **diag_dataset,
        **variable,
        **diag,
    }

    run_processor(
        task=task,
        work_dir=work_dir,
        config={},
    )


if __name__ == "__main__":
    main()
