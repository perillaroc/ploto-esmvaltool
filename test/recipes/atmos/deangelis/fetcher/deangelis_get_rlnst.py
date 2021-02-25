from pathlib import Path
import itertools

from esmvalcore.preprocessor._derive import get_required

from ploto_esmvaltool.fetcher.esmvalcore_fetcher import get_data
from ploto_esmvaltool.util.esmvaltool import (
    combine_variable,
    add_variable_info
)

from test.recipes.atmos.deangelis import (
    config as deangelis_config,
)

dataset = {
    "dataset": "FGOALS-g3",
    "exp": "piControl",
}


variable = {
    "short_name": "rlnst",
    "preprocessor": "spatial_mean",

    "project": "CMIP6",
    "ensemble": "r1i1p1f1",
    "mip": "Amon",
    "grid": "gn",
    "frequency": "mon",

    "start_year": 501,
    "end_year": 550,

    "derive": False,
    "force_derivation": False,
}


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case106/ploto"
    Path(work_dir).mkdir(parents=True, exist_ok=True)

    combined_variable = combine_variable(
        dataset=dataset,
        variable=variable,
    )
    # add_variable_info(combined_variable)

    # 需要的变量，来自 ESMValCore
    required_variables = get_required(
        short_name=combined_variable["short_name"],
        project=combined_variable["project"]
    )

    # 输入变量
    input_variables = [{
        **combined_variable,
        **v,
        "variable_group": f"{combined_variable['short_name']}_derive_input_{v['short_name']}",
        "alias": f"{combined_variable['dataset']}-{combined_variable['exp']}",
    } for v in required_variables]

    for v in input_variables:
        data_path = deangelis_config.data_path
        add_variable_info(v, override=True)

        task = {
            "products": [
                {
                    "variable": v,
                    "output": {
                        "output_directory": "{alias}/{variable_group}",
                        "output_data_source_file": "data_source.yml",
                    }
                }
            ],
            "config": {
                "data_path": data_path,
            },
            "output": {
                "output_directory": "{work_dir}/fetcher/preproc",
            }
        }

        config = {}

        get_data(
            task=task,
            work_dir=work_dir,
            config=config
        )


if __name__ == "__main__":
    main()
