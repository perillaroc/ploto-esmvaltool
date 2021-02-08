from ploto_esmvaltool.processor.esmvaltool_util_processor import run_processor

from test.recipes.atmos.climwip import recipe as climwip_recipe

base_dir = "/home/hujk/ploto/esmvaltool/cases/case105/ploto/"

def get_task(work_dir, variable):
    short_name = variable["short_name"]
    datasets = climwip_recipe.exp_datasets
    task = {
        "util_type": "combine_metadata",
        "metadata_files": [
            f"{base_dir}/graph/processor/preproc/{d['dataset']}/{short_name}/metadata.yml"
            for d in datasets
        ],
        "output_directory": f"{work_dir}/preproc/{short_name}"
    }
    return task


def main():
    work_dir = f"{base_dir}/graph/processor"
    variables = climwip_recipe.graph_variables

    tasks = [
        get_task(work_dir, v) for v in variables
    ]

    for task in tasks:
        run_processor(
            task=task,
            work_dir=work_dir,
            config={}
        )


if __name__ == "__main__":
    main()
