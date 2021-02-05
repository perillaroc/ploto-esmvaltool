from ploto_esmvaltool.processor.esmvaltool_util_processor import run_processor


base_dir = "/home/hujk/ploto/esmvaltool/cases/case105/ploto/"

def get_task(work_dir, variable_group):
    task = {
        "util_type": "combine_metadata",
        "metadata_files": [
            f"{base_dir}/map/processor/preproc/FGOALS-g3/{variable_group}/metadata.yml",
            f"{base_dir}/map/processor/preproc/CAMS-CSM1-0/{variable_group}/metadata.yml",
        ],
        "output_directory": f"{work_dir}/preproc/{variable_group}"
    }
    return task



def main():
    work_dir = f"{base_dir}/map/processor"

    tasks = [
        get_task(work_dir, variable_group) for variable_group in ["tas", "tas_reference"]
    ]

    for task in tasks:
        run_processor(
            task=task,
            work_dir=work_dir,
            config={}
        )


if __name__ == "__main__":
    main()
