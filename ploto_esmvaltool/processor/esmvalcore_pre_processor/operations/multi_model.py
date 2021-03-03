import typing

from esmvalcore.preprocessor._multimodel import (
    _multicube_statistics
)

from ploto_esmvaltool.processor.esmvalcore_pre_processor._product import Product


def run_multi_model_statistics(
        products: typing.List[Product],
        span,
        statistics,
        output_products=None,
        keep_input_datasets=True,
        **kwargs,
):
    cubes = [product.cubes for product in products]
    statistics_cubes = _multicube_statistics(
        cubes=cubes,
        span=span,
        statistics=statistics,
    )

    return products
