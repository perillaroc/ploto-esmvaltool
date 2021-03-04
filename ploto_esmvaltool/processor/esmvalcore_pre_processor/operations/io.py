import typing
from pathlib import Path

import iris
import yaml
from loguru import logger

from esmvalcore.preprocessor import save, load, concatenate
from esmvalcore.preprocessor._io import concatenate_callback


def run_load(
        product_input,
        product_variable,
        work_dir=".",
        **kwargs
) -> iris.cube.CubeList or typing.List[iris.cube.Cube]:
    if "input_data_source_file" in product_input:
        input_meta_file = product_input["input_data_source_file"].format(
            work_dir=work_dir,
            **product_variable
        )
        with open(input_meta_file, "r") as f:
            m = yaml.safe_load(f)
            input_files = m["input_files"]
    elif "input_metadata_files" in product_input:
        input_files = []
        for input_metadata_file in product_input["input_metadata_files"]:
            with open(input_metadata_file.format(
                    work_dir=work_dir,
                    **product_variable
            ), "r") as f:
                m = yaml.safe_load(f)
                for k in m:
                    input_files.append(k)
    else:
        raise ValueError("input source has not found. Please set input_files or input_data_source_file")

    callback = concatenate_callback

    cubes = []
    for f in input_files:
        logger.info(f"loading file: {f}")
        cube = load(
            f,
            callback
        )

        cubes.extend(cube)
    cube_list = iris.cube.CubeList(cubes)
    return cube_list


def run_concatenate(
        cubes: typing.Union[iris.cube.CubeList, typing.List[iris.cube.Cube]],
        **kwargs
) -> iris.cube.Cube:
    result = concatenate(cubes)
    return result


def run_save(
        cubes,
        product_variable: typing.Dict,
        product_output: typing.Dict,
        work_dir: str = ".",
        # file_path: typing.Union[str, Path] = None,
        **kwargs
) -> str:
    output_dir = Path(product_output["output_directory"].format(
        work_dir=work_dir,
        **product_variable,
    ))
    # output_dir.mkdir(parents=True, exist_ok=True)

    file_path = product_output.get("output_file", None)

    if file_path is None:
        file_path = _get_file_path(product_variable, output_dir)
    else:
        file_path = str(Path(output_dir, file_path)).format(
            work_dir=work_dir,
            **product_variable
        )

    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    return save(
        cubes=cubes,
        filename=file_path,
        **kwargs
    )


def _get_file_path(variable, output_dir):
    project = variable["project"]
    dataset = variable["dataset"]
    start_year = variable["start_year"]
    end_year = variable["end_year"]
    short_name = variable["short_name"]

    if project == "CMIP6":
        exp = variable["exp"]
        if isinstance(exp, typing.List) or isinstance(exp, typing.Tuple):
            exp = "-".join(exp)
        ensemble = variable["ensemble"]
        mip = variable["mip"]
        file_path = Path(
            output_dir,
            f"{project}_{dataset}_{mip}_{exp}_{ensemble}_{short_name}_{start_year}-{end_year}.nc"
        )
    elif project in ("OBS6", "obs4mips", "native6", "OBS"):
        version = variable["version"]
        mip = variable["mip"]
        data_type = variable["type"]
        file_path = Path(
            output_dir,
            f"{project}_{dataset}_{data_type}_{version}_{mip}_{short_name}_{start_year}-{end_year}.nc"
        )
    else:
        logger.error(f"project is not supported: {project}")
        raise ValueError(f"project is not supported: {project}")

    return file_path


def run_write_metadata(
        product_variable: typing.Dict,
        product_output: typing.Dict,
        work_dir: typing.Union[Path, str],
        file_path: typing.Union[Path, str],
        metadata_file_name: typing.Union[Path, str]="metadata.yml",
        **kwargs,
) -> Path:
    output_dir = Path(product_output["output_directory"].format(
        work_dir=work_dir,
        **product_variable,
    ))
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = Path(file_path).absolute()

    project = product_variable["project"]


    if project == "CMIP6":
        exp = product_variable["exp"]
        if isinstance(exp, typing.List):
            exp = "-".join(exp)
        product_variable["exp"] = exp
    elif project in ("OBS6", "native6", "obs4mips", "OBS"):
        pass
    else:
        raise ValueError(f"project is not supported: {project}")

    meta_data = {
        **product_variable,
        "filename": str(file_path),
    }

    meta_data_path = Path(output_dir, metadata_file_name)

    with open(meta_data_path, "w") as f:
        yaml.safe_dump({
            str(file_path): meta_data,
        }, f)

    return meta_data_path
