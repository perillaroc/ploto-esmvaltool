from ploto_esmvaltool.processor.esmvaltool_util_processor import run_processor


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case2/ploto/processor"

    short_name = "tasmax"

    exps = [
        "historical",
        "ssp119"
    ]

    task = {
        "util_type": "combine_metadata",
        "metadata_files": [
            f"{work_dir}/preproc/{exp}/{short_name}/metadata.yml"
            for exp in exps
        ],
        "output_directory": f"{work_dir}/preproc/{short_name}"
    }

    run_processor(
        task=task,
        work_dir=work_dir,
        config={}
    )


if __name__ == "__main__":
    main()
