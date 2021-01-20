from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor

from loguru import logger


def main():
    work_dir = "./dist/tests/esmvalcore_pre_processor"
    operations = [
        {
            "type": "load",
        },
        {
            "type": "fix_metadata",
        },
        {
            "type": "concatenate",
        },
        {
            "type": "cmor_check_metadata",
        },
        {
            "type": "clip_start_end_year"
        },
        {
            "type": "fix_data"
        },
        {
            "type": "cmor_check_data"
        }
    ]

    task = {
        # input files
        "input_meta_file": "./test/esmvalcore_pre_processor/input_meta_file.yml",

        # operations
        "operations": operations,

        # settings
        "dataset": "FGOALS-g3",
        "project": "CMIP6",
        "mip": "day",
        "exp": "1pctCO2",
        "ensemble": "r1i1p1f1",
        "grid": "gn",

        "frequency": "day",

        "start_year": 370,
        "end_year": 390,

        # parameter
        "short_name": "pr",

        # output
        "output_directory": "preproc/pr"
    }

    run_processor(
        task=task,
        work_dir=work_dir,
        config={},
    )


if __name__ == "__main__":
    main()
