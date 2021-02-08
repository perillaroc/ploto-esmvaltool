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
        "run_base_dir": "/home/hujk/ploto/ploto-esmvaltool/dist/cases/case105/run"
    }
}

plot_config = {
    "log_level": "info",
    "write_netcdf": True,
    "write_plots": True,
    "output_file_type": "png",
    "profile_diagnostic": False,
    "auxiliary_data_dir": "/home/hujk/ploto/esmvaltool/cases/case1/case1.2/auxiliary_data"
}