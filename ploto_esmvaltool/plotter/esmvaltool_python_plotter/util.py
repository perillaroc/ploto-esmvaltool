from esmvalcore._recipe import Recipe
from esmvalcore._config import (
    read_config_user_file,
)


def generate_script_settings(
        raw_recipe: dict,
        config_file: str,
        recipe_file: str,
        diagnostic_name: str,
        script_name: str,
) -> dict:
    """
    Generate diagnostic script settings using esmvalcore.Recipe

    Parameters
    ----------
    raw_recipe: dict
    config_file: str
        config_file_path
    recipe_file: str
        recipe file path.
    diagnostic_name: str
    script_name: str

    Returns
    -------
    dict:
        script settings
        {
            # from diagnostic setting
            'quickplot': {
                'plot_type': 'pcolormesh'
            },

            # added by Recipe
            'recipe': 'recipe.yml',
            'version': '2.0.0b5',
            'script': 'script1',

            # from config_user
            'run_dir': '/some/path/recipe_20200303_022547/run/diagnostic1/script1',
            'plot_dir': '/some/path/recipe_20200303_022547/plots/diagnostic1/script1',
            'work_dir': '/some/path/recipe_20200303_022547/work/diagnostic1/script1',

            'max_data_filesize': 100,
            'output_file_type': 'png',
            'log_level': 'info',
            'write_plots': True,
            'write_netcdf': True,
            'profile_diagnostic': False,
            'auxiliary_data_dir': '/some/path/auxiliary_data',

            # from diagnostic setting
            'themes': ['phys'],
            'realms': ['atmos']
        }
    """
    config_user = read_config_user_file(config_file=config_file, recipe_name="recipe")

    recipe = Recipe(
        raw_recipe,
        config_user,
        initialize_tasks=False,
        recipe_file=recipe_file,
    )

    diagnostics = recipe.diagnostics
    return diagnostics[diagnostic_name]["scripts"][script_name]["settings"]
