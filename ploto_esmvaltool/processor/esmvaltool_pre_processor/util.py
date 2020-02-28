from esmvalcore._recipe import Recipe
from esmvalcore._config import (
    configure_logging,
    read_config_user_file,
)


def generate_variables(
        raw_recipe: dict,
        config_file: dict,
        recipe_file: str,
        raw_variable: dict,
        raw_datasets: list
) -> list:
    config_user = read_config_user_file(config_file=config_file, recipe_name="recipe")
    recipe = Recipe(
        raw_recipe,
        config_user,
        initialize_tasks=False,
        recipe_file=recipe_file,
    )

    return recipe._initialize_variables(
        raw_variable=raw_variable,
        raw_datasets=raw_datasets,
    )
