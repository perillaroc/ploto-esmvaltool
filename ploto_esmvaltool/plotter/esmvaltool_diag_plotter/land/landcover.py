import typing


def generate_default_plot_task(name, **kwargs) -> typing.Dict:
    return generate_plot(name, **kwargs)


def generate_plot(
        name,
        **kwargs
) -> typing.Dict:
    return {
        "diagnostic": {
            "recipe": "recipe_spei.yml",
            "name": name,
        },

        "input_files": [
        ],

        "diagnostic_script": {
            "path": {
                "group": "base",
                "script": "landcover/albedolandcover.py",
            },
            "settings": {
                "script": "albedolandcover",
                "params": {
                    "latsize_BB": 5,
                    "lonsize_BB": 5,
                    "threshold_sumpred": 90,
                    "mingc": 2,
                    "minnum_gc_bb": 15,
                    "snowfree": True,
                    "lc1_class": ['treeFrac'],
                    "lc2_class": ['shrubFrac'],
                    "lc3_class": ['grassFrac', 'cropFrac', 'pastureFrac'],
                }
            }
        }
    }