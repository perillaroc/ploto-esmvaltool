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

    return get_levels(
        combined_variable,
        output_directory="{work_dir}" + f"/{diagnostic_name}/fetcher/preproc/{combined_variable['alias']}/{combined_variable['variable_group']}",
        work_dir=work_dir,
        config=config
    )


def get_levels(variable, output_directory, work_dir, config):
    selected_files = get_selected_files(
        variable, config
    )
    reference_file = selected_files[0]

    levels = get_reference_levels(
        reference_file,
        project=variable["project"],
        dataset=variable["dataset"],
        short_name=variable["short_name"],
        mip=variable["mip"],
        frequency=variable["frequency"],
        fix_dir=output_directory
    )
    return levels
