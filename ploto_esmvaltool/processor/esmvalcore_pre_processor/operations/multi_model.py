import typing
import copy

from esmvalcore.preprocessor._multimodel import (
    _multicube_statistics
)

from ploto_esmvaltool.processor.esmvalcore_pre_processor._product import Product


def run_multi_model_statistics(
        products: typing.Set[Product],
        span: str,
        statistics: typing.List,
        output: typing.Dict,
        keep_input_datasets: bool=True,
        **kwargs,
):
    cubes = [cube for product in products for cube in product.cubes]
    statistics_cubes = _multicube_statistics(
        cubes=cubes,
        span=span,
        statistics=statistics,
    )

    variable = list(products)[0].variable

    statistics_products = set()
    for statistics_operator, cube in statistics_cubes.items():
        p_variable = copy.deepcopy(variable)
        dataset = f"MultiModel{statistics_operator.capitalize()}"
        p_variable.update({
            "dataset": dataset,
            "alias": dataset,
            "operator": statistics_operator
        })

        p = Product(
            cubes=[cube],
            output=output,
            variable=p_variable
        )
        statistics_products.add(p)

    if keep_input_datasets:
        return products | statistics_products
    else:
        return statistics_products
