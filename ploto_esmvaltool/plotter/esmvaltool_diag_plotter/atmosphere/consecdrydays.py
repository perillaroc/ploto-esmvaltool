


def generate_default_task():
    task = {
        "diag": {
            "dryindex": "cdd",
            "frlim": 5,
            "plim": 1,
            "quickplot": {
                "plot_type": "pcolormesh",
            },
            "recipe": "recipe_consecdrydays.yml",
            "script": "consecutive_dry_days"
        },

        "input_files": [
            "{work_dir}/preproc/pr/metadata.yml"
        ],

        "diag_script": {
            "group": "base",
            "name": "droughtindex/diag_cdd.py",
        },
    }

    return task
