from ploto_esmvaltool.processor.esmvaltool_util_processor import run_processor


base_dir = "/home/hujk/ploto/esmvaltool/cases/case105/ploto"

def get_task(work_dir, short_name):
    task = {
        "util_type": "combine_metadata",
        "metadata_files": [
            f"{base_dir}/processor/preproc/FGOALS-g3/historical/{short_name}/metadata.yml",
            f"{base_dir}/processor/preproc/CAMS-CSM1-0/historical/{short_name}/metadata.yml",
            f"{base_dir}/processor/preproc/ERA5/{short_name}/metadata.yml"
        ],
        "output_directory": f"{work_dir}/preproc/{short_name}"
    }
    return task



def main():
    work_dir = f"{base_dir}/processor"

    tasks = [
        get_task(work_dir, short_name) for short_name in ["tas", "psl", "pr"]
    ]

    for task in tasks:
        run_processor(
            task=task,
            work_dir=work_dir,
            config={}
        )


if __name__ == "__main__":
    main()
