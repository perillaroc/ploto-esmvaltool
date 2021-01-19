from ploto_esmvaltool.processor.esmvalcore_pre_processor import operations as esmvalcore_operations

from loguru import logger


def main():
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
            "type": "fix_data"
        },
        {
            "type": "cmor_check_data"
        }
    ]

    task = {
        # input files
        "input_meta_file": "./input_meta_file.yml",

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
    }

    cube = None
    for step in operations:
        op = step["type"]
        logger.info(f"run step {op}")
        fun = getattr(esmvalcore_operations, f"run_{op}")
        cube = fun(
            operation=step,
            task=task,
            cube=cube
        )
    print(cube)




if __name__ == "__main__":
    main()
