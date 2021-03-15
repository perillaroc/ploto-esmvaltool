config = {
    "esmvaltool": {
        "executables": {
            "py": "/home/hujk/anaconda3/envs/wangdp-esm/bin/python",
            "r": "/home/hujk/anaconda3/envs/wangdp-esm/bin/Rscript",
            "ncl": "/home/hujk/anaconda3/envs/wangdp-esm/bin/ncl",
        },
        "recipes": {
            "base": "/home/hujk/ploto/esmvaltool/study/esmvaltool/ESMValTool/esmvaltool/recipes",
        },
        "diag_scripts": {
            "base": "/home/hujk/ploto/esmvaltool/study/esmvaltool/ESMValTool/esmvaltool/diag_scripts",
        },
    },
    "base": {
        "run_base_dir": "/home/hujk/ploto/esmvaltool/cases/case109/run"
    }
}

plot_config = {
    "log_level": "info",
    "write_netcdf": True,
    "write_plots": True,
    "output_file_type": "png",
    "profile_diagnostic": False,
    "auxiliary_data_dir": "/home/hujk/ploto/esmvaltool/cases/auxiliary_data"
}

data_path = {
    "CMIP6": [
        "/data/brick/b1/CMIP6_DATA",
        "/home/hujk/clusterfs/wangdp/data/CMIP6"
    ],
    "OBS6": [
        "/data/brick/b2/OBS/esmvaltool_output/cmorize_obs_20210202_083242"
    ],
    "native6": [
        "/home/hujk/clusterfs/wangdp/data/rawobs"
    ],
    "obs4mips": [
        "/home/hujk/clusterfs/wangdp/data/obs4mips"
    ],
    "OBS": [
        "/home/hujk/clusterfs/wangdp/data/obs"
    ]
}
