from pathlib import Path
import inspect

import ploto_esmvaltool.processor.esmvalcore_pre_processor.operations as esmvalcore_operations
from .operations.util import _get_settings
from .operations import (
    run_load,
    run_save,
    run_write_metadata,
)
from ploto.logger import get_logger

import attr
import iris

logger = get_logger()


@attr.s(eq=False)
class Product(object):
    variable = attr.ib(default=None)
    input = attr.ib(default=None)
    output = attr.ib(default=None)
    settings = attr.ib(default=None)
    cubes = attr.ib(default=None)

    def update_output(
            self,
            output,
    ):
        # TODO: use update_product_output()
        output_directory = output.get("output_directory", "")
        product_output_directory = self.output.get("output_directory", "")
        output_directory = str(Path(
            output_directory,
            product_output_directory
        ))

        self.output["output_directory"] = output_directory

    def add_diagnostic(self, diagnostic):
        self.variable = {
            **self.variable,
            **diagnostic,
        }

    def run_operation_block(
            self,
            operation_block,
            work_dir,
    ):
        if self.cubes is None:
            self.cubes = self.load(work_dir=work_dir)

        # run steps
        for step in operation_block:
            op = step["type"]
            logger.info(f"run step {op}")
            settings = _get_settings(step, self.settings)

            if settings is None:
                continue

            fun = getattr(esmvalcore_operations, f"run_{op}")
            first_argument = inspect.getfullargspec(fun).args[0]
            result = []
            if first_argument.endswith("s"):
                result.append(fun(
                    # operation=step,
                    self.cubes,
                    variable=self.variable,
                    settings=settings,
                    work_dir=work_dir,
                ))
            else:
                for cube in self.cubes:
                    result.append(
                        fun(
                            cube,
                            variable=self.variable,
                            settings=settings,
                            work_dir=work_dir,
                        )
                    )

            cubes = []
            for item in result:
                if isinstance(item, (iris.cube.Cube)):
                    cubes.append(item)
                else:
                    cubes.extend(item)
            self.cubes = cubes

        # save to workdir
        file_path = self.save(work_dir=work_dir)
        logger.info(f"write file to {file_path}")

        # write metadata
        metadata = self.write_metadata(file_path, work_dir=work_dir)
        logger.info(f"write metadata to {metadata.absolute()}")

    def load(self, work_dir):
        cubes = run_load(
            product_input=self.input,
            product_variable=self.variable,
            work_dir=work_dir,
        )
        return cubes

    def save(self, work_dir):
        # TODO: use cubes in Product!
        cubes = self.cubes
        if isinstance(cubes, iris.cube.Cube):
            cubes = [cubes]
        file_path = run_save(
            cubes=cubes,
            product_variable=self.variable,
            product_output=self.output,
            work_dir=work_dir,
        )
        return file_path

    def write_metadata(self, file_path, work_dir):
        output_metadata_file_name = self.output.get(
            "output_metadata_file_name", "metadata.yml"
        )
        metadata = run_write_metadata(
            product_variable=self.variable,
            product_output=self.output,
            work_dir=work_dir,
            file_path=file_path,
            metadata_file_name=output_metadata_file_name,
        )
        return metadata

    def wasderivedfrom(self, product):
        """
        For PreprocessorFile in ESMValCore.
        """
        pass

    def copy_provenance(self):
        return self

    @property
    def filename(self):
        return None



def update_product_output(
        product_output,
        output,
):
    output_directory = output.get("output_directory", "")
    product_output_directory = product_output.get("output_directory", "")
    output_directory = str(Path(
        output_directory,
        product_output_directory
    ))

    product_output["output_directory"] = output_directory
    return product_output
