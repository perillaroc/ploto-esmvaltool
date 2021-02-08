from ploto_esmvaltool.processor.esmvaltool_util_processor import run_processor

from test.recipes.atmos.climwip import recipe as climwip_recipe


base_dir = "/home/hujk/ploto/esmvaltool/cases/case105/ploto/"

def get_task(work_dir, variable):
    variable_group = variable["variable_group"]
    task = {
        "util_type": "combine_metadata",
        "metadata_files": [
            f"{base_dir}/map/processor/preproc/{d['dataset']}/{variable_group}/metadata.yml"
            for d in climwip_recipe.exp_datasets
        ],
        "output_directory": f"{work_dir}/preproc/{variable_group}"
    }
    return task



def main():
    work_dir = f"{base_dir}/map/processor"

    tasks = [
        get_task(work_dir, variable) for variable in climwip_recipe.map_variables
    ]

    for task in tasks:
        run_processor(
            task=task,
            work_dir=work_dir,
            config={}
        )


if __name__ == "__main__":
    main()
