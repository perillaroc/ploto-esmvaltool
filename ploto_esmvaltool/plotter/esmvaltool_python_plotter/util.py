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
