import yaml

from ploto_esmvaltool.processor.esmvaltool_pre_processor import run_processor
from ploto_esmvaltool.processor.esmvaltool_pre_processor.util import generate_variables


def test_esmvaltool_pre_processor():
    work_dir = "./dist/cases/case1/run"

    # load from config.yml
    config = {
        # data dirs
        'rootpath': {
            'CMIP5': [
                '/home/hujk/ploto/esmvaltool/data/cmip5',
                '/data/brick/b3/cmip5/disk1/CanESM2/CanESM2_Amon_historical_r1i1p1_output1',
                '/data/brick/b4/cmip5/disk6/historical/mon/atmos/ta/r1i1p1',
                '/data/brick/b4/cmip5/disk6/historical/mon/atmos/pr/r1i1p1'
            ],
            'CMIP6': [
                '/home/hujk/ploto/esmvaltool/data/cmip6'
            ],
            'OBS': '/home/hujk/ploto/esmvaltool/data/obs',
            'RAWOBS': '/home/hujk/ploto/esmvaltool/data/rawobs',
            'default': '/home/hujk/ploto/esmvaltool/data/default'
        },
        'drs': {
            'CMIP5': 'default',
            'CMIP6': 'default'
        },
        'auxiliary_data_dir': '/home/hujk/ploto/esmvaltool/cases/case5/case5.1/auxiliary_data',

        # output dir
        'output_dir': work_dir,  # 会被esmvalcore替换掉，需要在processor中手动修改

        # settings
        'max_parallel_tasks': 1,
        'write_plots': True,
        'write_netcdf': True,
        'log_level': 'info',
        'exit_on_warning': False,
        'output_file_type': 'png',
        'compress_netcdf': False,
        'save_intermediary_cubes': True,
        'remove_preproc_dir': False,
        'profile_diagnostic': False,

        'write_ncl_interface': False,
    }

    # load recipe.yml
    recipe_file_path = "./dist/recipe.yml"
    with open(recipe_file_path, "r") as f:
        raw_recipe = yaml.safe_load(f)

    raw_variable = {
        # from recipe["diagnostics"]["diagnostic1"]["variables"]["ta"]
        'preprocessor': 'preprocessor1',

        # added by esmvalcore.Recipe, values are all from recipe
        "variable_group": "ta",
        "short_name": "ta",
        "diagnostic": "diagnostic1",
    }

    # load from recipe["datasets"] + diagnostic's additional datasets from recipe
    raw_datasets = [
        {
            'dataset': 'CanESM2',
            'project': 'CMIP5',
            'mip': 'Amon',
            'exp': 'historical',
            'ensemble': 'r1i1p1',
            'start_year': 1996,
            'end_year': 1998,
        },
        {
            'dataset': 'FGOALS-g2',
            'project': 'CMIP5',
            'mip': 'Amon',
            'exp': 'historical',
            'ensemble': 'r1i1p1',
            'start_year': 1996,
            'end_year': 1998,
        }
    ]

    config_file = "./dist/config.yml"
    variables = generate_variables(
        raw_recipe=raw_recipe,
        config_file=config_file,
        recipe_file="recipe.yml",
        raw_variable=raw_variable,
        raw_datasets=raw_datasets,
    )

    # from recipe["documentation"]
    recipe_documentation = {
        'description': 'Example recipe that plots the mean precipitation and temperature.\n',
        'authors': ['andela_bouwe', 'righi_mattia'],
        'maintainer': ['schlund_manuel'],
        'references': ['acknow_project'],
        'projects': ['esmval', 'c3s-magic']
    }

    # from recipe["preprocessors"] + default
    profiles = {
        "preprocessor1": {
            "extract_levels": {
                "levels": 85000,
                "scheme": "nearest",
            },
            "regrid": {
                "target_grid": "1x1",
                "scheme": "linear",
            },
            "multi_model_statistics": {
                "span": "overlap",
                "statistics": ["mean", "median"],
            }
        },
        "default": {},
    }

    run_processor(
        task={
            "step_type": "processor",
            "type": "ploto_esmvaltool.processor.esmvaltool_pre_processor",
            "task_name": "diagnostics/ta",
            "variables": variables,
            "profiles": profiles,
            "config": config,
            "recipe_name": "recipe.yml",
            "recipe_documentation": recipe_documentation,
        },
        work_dir=work_dir,
        config={},
    )


if __name__ == "__main__":
    test_esmvaltool_pre_processor()
