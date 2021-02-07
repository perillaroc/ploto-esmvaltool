import itertools
from pathlib import Path

from ploto_esmvaltool.plotter.esmvaltool_diag_plotter.atmosphere.climwip import (
    generate_climatological_mean_operations
)
from ploto.run import run_ploto


data_path = {
    "CMIP6": [
        "/home/hujk/clusterfs/wangdp/data/CMIP6"
    ],
    "OBS6": [
        #"/home/hujk/clusterfs/wangdp/data/obs"
        "/data/brick/b2/OBS/esmvaltool_output/cmorize_obs_20210119_071639"
    ],
    "native6": [
        "/home/hujk/clusterfs/wangdp/data/rawobs"
    ]
}


def get_weights_fetcher(
        dataset,
        exp,
        start_year,
        end_year,
        short_name
):
    dataset = {
        "dataset": dataset,
        "project": "CMIP6",
        "mip": "Amon",
        "exp": exp,
        "ensemble": "r1i1p1f1",
        "grid": "gn",
        "frequency": "mon",

        "start_year": start_year,
        "end_year": end_year,
    }

    variables = [
        {
            "short_name": short_name,
        }
    ]

    task = {
        "dataset": dataset,
        "variables": variables,
        "data_path": data_path,

        "output_directory": "{work_dir}" + f"/weights/fetcher/preproc/{dataset['dataset']}/{short_name}",
        "output_data_source_file": "data_source.yml",

        "step_type": "fetcher",
        "type": "ploto_esmvaltool.fetcher.esmvalcore_fetcher",
    }
    return task


def get_weights_era5_fetcher(
        start_year,
        end_year,
        short_name
):
    dataset = {
        "dataset": "ERA5",
        "project": "native6",
        "type": "reanaly",
        "version": 1,
        "tier": 3,

        "mip": "Amip",
        "frequency": "mon",

        "start_year": start_year,
        "end_year": end_year,
    }

    variables = [
        {
            "short_name": short_name,
        }
    ]

    task = {
        "dataset": dataset,
        "variables": variables,
        "data_path": data_path,

        "output_directory": "{work_dir}" + f"/weights/fetcher/preproc/{dataset['dataset']}/{short_name}",
        "output_data_source_file": "data_source.yml",

        "step_type": "fetcher",
        "type": "ploto_esmvaltool.fetcher.esmvalcore_fetcher",
    }
    return task


def get_graph_fetcher(
        dataset,
        exp,
        start_year,
        end_year,
        short_name
):
    dataset = {
        "dataset": dataset,
        "project": "CMIP6",
        "mip": "Amon",
        "exp": exp,
        "ensemble": "r1i1p1f1",
        "grid": "gn",
        "frequency": "mon",

        "start_year": start_year,
        "end_year": end_year,
    }

    variables = [
        {
            "short_name": short_name,
        }
    ]

    task = {
        "dataset": dataset,
        "variables": variables,
        "data_path": data_path,

        "output_directory": "{work_dir}" + f"/graph/fetcher/preproc/{dataset['dataset']}/{short_name}",
        "output_data_source_file": "data_source.yml",

        "step_type": "fetcher",
        "type": "ploto_esmvaltool.fetcher.esmvalcore_fetcher",
    }

    return task


def get_map_tas_fetcher(
        dataset,
        exp,
        start_year,
        end_year,
        short_name
):
    dataset = {
        "dataset": dataset,
        "project": "CMIP6",
        "mip": "Amon",
        "exp": exp,
        "ensemble": "r1i1p1f1",
        "grid": "gn",
        "frequency": "mon",

        "start_year": start_year,
        "end_year": end_year,
    }

    variables = [
        {
            "short_name": short_name,
        }
    ]

    task = {
        "dataset": dataset,
        "variables": variables,
        "data_path": data_path,

        "output_directory": "{work_dir}" + f"/map/fetcher/preproc/{dataset['dataset']}/{short_name}",
        "output_data_source_file": "data_source.yml",

        "step_type": "fetcher",
        "type": "ploto_esmvaltool.fetcher.esmvalcore_fetcher",
    }
    return task


def get_fetcher_steps():
    steps = []

    variables = ["tas", "psl", "pr"]
    datasets = ["FGOALS-g3", "CAMS-CSM1-0"]

    tasks = [
       {
            "dataset": d,
            "exp": ["historical", "ssp585"],
            "short_name": v,
            "start_year": 1995,
            "end_year": 2015
        }
        for v, d in itertools.product(variables, datasets)
    ]
    steps.extend([get_weights_fetcher(**task) for task in tasks])

    tasks = [
        {
            "short_name": v,
            "start_year": 1995,
            "end_year": 2014
        } for v in ["tas", "pr", "psl"]
    ]
    steps.extend([get_weights_era5_fetcher(**task) for task in tasks])

    tasks = [
        {
            "dataset": d,
            "exp": ["historical", "ssp585"],
            "short_name": "tas",
            "start_year": 1960,
            "end_year": 2099
        }
        for d in datasets
    ]
    steps.extend([get_graph_fetcher(**task) for task in tasks])


    variables = ["tas"]
    tasks = [
        {
            "dataset": d,
            "exp": ["historical", "ssp585"],
            "short_name": v,
            "start_year": 2081,
            "end_year": 2099
        }
        for v, d in itertools.product(variables, datasets)
    ]
    steps.extend([get_map_tas_fetcher(**task) for task in tasks])


    return steps


def get_processor_steps():
    steps = []
    return steps


def get_plotter_steps():
    steps = []
    return steps


def run_climwip():
    steps = []
    steps.extend(get_fetcher_steps())
    steps.extend(get_processor_steps())
    steps.extend(get_plotter_steps())

    config = {
        "esmvaltool": {
            "executables": {
                "py": "/home/hujk/anaconda3/envs/wangdp-esm/bin/python",
                "r": "/home/hujk/anaconda3/envs/wangdp-esm/bin/Rscript"
            },
            "recipes": {
                "base": "/home/hujk/ploto/esmvaltool/study/esmvaltool/ESMValTool/esmvaltool/recipes",
            },
            "diag_scripts": {
                "base": "/home/hujk/ploto/esmvaltool/study/esmvaltool/ESMValTool/esmvaltool/diag_scripts",
            },
        },
        "base": {
            "run_base_dir": "/home/hujk/ploto/esmvaltool/cases/case105/run"
        }
    }
    Path(config["base"]["run_base_dir"]).mkdir(parents=True, exist_ok=True)

    run_ploto({
        "data": {
            "steps": steps
        }
    }, config)



if __name__ == "__main__":
    run_climwip()
