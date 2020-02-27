from ploto_esmvaltool.processor.esmvaltool_pre_processor import run_processor


def test_esmvaltool_pre_processor():
    variables = [
        {
            'preprocessor': 'preprocessor1',
            'diagnostic': 'diagnostic1',
            'variable_group': 'ta',
            'short_name': 'ta',
            'standard_name': 'air_temperature',
            'long_name': 'Air Temperature',
            'units': 'K',

            'institute': ['CCCma'],
            'dataset': 'CanESM2',
            'project': 'CMIP5',
            'cmor_table': 'CMIP5',
            'mip': 'Amon',
            'exp': 'historical',
            'ensemble': 'r1i1p1',
            'frequency': 'mon',
            'modeling_realm': ['atmos'],

            'start_year': 1996,
            'end_year': 1998,

            'recipe_dataset_index': 0,
            'alias': 'CanESM2',

            'filename': (
                '/home/hujk/ploto/esmvaltool/cases/case5/case5.1/esmvaltool_output/'
                'recipe_20200227_024352/preproc/diagnostic1/ta/CMIP5_CanESM2_Amon_historical_r1i1p1_ta_1996-1998.nc'
            )
        },
        {
            'preprocessor': 'preprocessor1',
            'diagnostic': 'diagnostic1',
            'variable_group': 'ta',
            'short_name': 'ta',
            'standard_name': 'air_temperature',
            'long_name': 'Air Temperature',
            'units': 'K',

            'institute': ['LASG-CESS'],
            'dataset': 'FGOALS-g2',
            'project': 'CMIP5',
            'cmor_table': 'CMIP5',
            'mip': 'Amon',
            'exp': 'historical',
            'ensemble': 'r1i1p1',
            'frequency': 'mon',
            'modeling_realm': ['atmos'],

            'start_year': 1996,
            'end_year': 1998,

            'recipe_dataset_index': 1,
            'alias': 'FGOALS-g2',

            'filename': (
                '/home/hujk/ploto/esmvaltool/cases/case5/case5.1/esmvaltool_output/'
                'recipe_20200227_024352/preproc/diagnostic1/ta/CMIP5_FGOALS-g2_Amon_historical_r1i1p1_ta_1996-1998.nc'
            )
        }
    ]
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
    config_user = {
        'rootpath': {
            'CMIP5': [
                '/home/hujk/ploto/esmvaltool/data/cmip5',
                '/data/brick/b3/cmip5/disk1/CanESM2/CanESM2_Amon_historical_r1i1p1_output1',
                '/data/brick/b4/cmip5/disk6/historical/mon/atmos/ta/r1i1p1',
                '/data/brick/b4/cmip5/disk6/historical/mon/atmos/pr/r1i1p1'],
            'CMIP6': ['/home/hujk/ploto/esmvaltool/data/cmip6'],
            'OBS': ['/home/hujk/ploto/esmvaltool/data/obs'],
            'RAWOBS': ['/home/hujk/ploto/esmvaltool/data/rawobs'],
            'default': ['/home/hujk/ploto/esmvaltool/data/default']
        },
        'drs': {'CMIP5': 'default', 'CMIP6': 'default'},

        'preproc_dir': '/home/hujk/ploto/esmvaltool/cases/case5/case5.1/esmvaltool_output/recipe_20200227_024352/preproc',
        'work_dir': '/home/hujk/ploto/esmvaltool/cases/case5/case5.1/esmvaltool_output/recipe_20200227_024352/work',
        'plot_dir': '/home/hujk/ploto/esmvaltool/cases/case5/case5.1/esmvaltool_output/recipe_20200227_024352/plots',
        'run_dir': '/home/hujk/ploto/esmvaltool/cases/case5/case5.1/esmvaltool_output/recipe_20200227_024352/run',
        'output_dir': '/home/hujk/ploto/esmvaltool/cases/case5/case5.1/esmvaltool_output/recipe_20200227_024352',
        'auxiliary_data_dir': '/home/hujk/ploto/esmvaltool/cases/case5/case5.1/auxiliary_data',

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
        'max_data_filesize': 100,
        'run_diagnostic': True,
        'config_developer_file': None,
        'skip-nonexistent': False,
        'diagnostics': set(),
        'synda_download': False,
        'write_ncl_interface': False
    }
    recipe_documentation = {
        'description': 'Example recipe that plots the mean precipitation and temperature.\n',
        'authors': ['andela_bouwe', 'righi_mattia'],
        'maintainer': ['schlund_manuel'],
        'references': ['acknow_project'],
        'projects': ['esmval', 'c3s-magic']
    }

    run_processor(
        task={
            "step_type": "processor",
            "type": "ploto_esmvaltool.processor.esmvaltool_pre_processor",
            "task_name": "diagnostics/ta",
            "variables": variables,
            "profiles": profiles,
            "config_user": config_user,
            "recipe_name": "recipe.yml",
            "recipe_documentation": recipe_documentation,
        },
        work_dir="./dist/cases/case1/run",
        config={},
    )


if __name__ == "__main__":
    test_esmvaltool_pre_processor()
