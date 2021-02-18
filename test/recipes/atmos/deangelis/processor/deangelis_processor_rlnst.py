import itertools
from pathlib import Path

from ploto_esmvaltool.processor.esmvalcore_pre_processor import run_processor
from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.deangelis import (
    generate_default_operations
)

from test.recipes.atmos.deangelis import (
    config as deangelis_config,
    recipe as deangelis_recipe,
)

from esmvalcore.preprocessor._derive import get_required


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


    operations = generate_default_operations(name=variable["preprocessor"])
    settings = deangelis_recipe.processor_settings[variable["preprocessor"]]

    diag_dataset = {
        "modeling_realm": [
            "atmos"
        ],
    }

    diag = {
        "diagnostic": "deangelisf1b",
    }



    combined_variable = {
        **dataset,
        **variable,
    }

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
        task = {
            "input_data_source_file": "{work_dir}" + f"/fetcher/preproc/{v['alias']}/{v['variable_group']}/data_source.yml",
            # output
            "output_directory": "{work_dir}" + f"/processor/preproc/{v['alias']}/{v['variable_group']}",

            # operations
            "operations": operations,

            "dataset": v,
            "diagnostic_dataset": diag_dataset,
            "variable": v,
            "diagnostic": diag,
            "settings": settings
        }

        config = {}

        run_processor(
            task=task,
            work_dir=work_dir,
            config=config
        )


if __name__ == "__main__":
    main()
