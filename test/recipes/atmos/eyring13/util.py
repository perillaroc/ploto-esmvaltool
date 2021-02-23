from ploto_esmvaltool.fetcher.esmvalcore_fetcher import get_selected_files

from esmvalcore.preprocessor._regrid import get_reference_levels

from test.recipes.atmos.eyring13 import (
    config as eyring13_config,
    recipe as eyring13_recipe,
)


diagnostic_name = "fig12"


def update_levels(settings, work_dir, config):
    extract_levels = settings.get("extract_levels", None)
    if extract_levels is None:
        return
    levels = extract_levels.get("levels", None)
    if levels is None:
        return

    if levels == "reference_dataset":
        settings["extract_levels"]["levels"] = get_processor_levels(
            work_dir, config
        )
    return settings


def get_processor_levels(work_dir, config):
    variable = eyring13_recipe.variables[0]
    reference_dataset = eyring13_recipe.variable_additional_datasets["ua"][0]

    combined_variable = {
        **variable,
        **reference_dataset
    }
    combined_variable["alias"] = f"{combined_variable['dataset']}-{combined_variable['exp']}"

    task = {
        "dataset": combined_variable,
        "variables": [combined_variable],

        "output_directory": "{work_dir}" + f"/{diagnostic_name}/fetcher/preproc/{combined_variable['alias']}/{combined_variable['variable_group']}",
        "data_path": eyring13_config.data_path
    }
    return get_levels(
        task,
        work_dir,
        config
    )


def get_levels(task, work_dir, config):
    selected_files = get_selected_files(
        task, work_dir, config
    )
    reference_file = selected_files[0]

    combined_variable = task["dataset"]
    levels = get_reference_levels(
        reference_file,
        project=combined_variable["project"],
        dataset=combined_variable["dataset"],
        short_name=combined_variable["short_name"],
        mip=combined_variable["mip"],
        frequency=combined_variable["frequency"],
        fix_dir=task["output_directory"]
    )
    return levels
