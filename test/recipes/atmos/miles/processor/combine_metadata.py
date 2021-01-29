from ploto_esmvaltool.processor.esmvaltool_util_processor import run_processor


def main():
    work_dir = "/home/hujk/ploto/esmvaltool/cases/case3/ploto/processor"

    tasks = [{
            "util_type": "combine_metadata",
            "metadata_files": [
                "/home/hujk/ploto/esmvaltool/cases/case3/ploto/processor/preproc/historical/zg/metadata.yml",
                "/home/hujk/ploto/esmvaltool/cases/case3/ploto/processor/preproc/ERA-Interim/zg/metadata.yml"
            ],
            "output_directory": f"{work_dir}/preproc/"
        }
    ]

    for task in tasks:
        run_processor(
            task=task,
            work_dir=work_dir,
            config={}
        )


if __name__ == "__main__":
    main()
