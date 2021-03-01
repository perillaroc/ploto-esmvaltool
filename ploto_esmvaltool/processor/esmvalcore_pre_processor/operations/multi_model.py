from esmvalcore.preprocessor._multimodel import _multiproduct_statistics


def run_multi_model_statistics(
        products,
        span,
        statistics,
        output_products=None,
        keep_input_datasets=True,
        **kwargs,
):
    products = _multiproduct_statistics(
        products=products,
        span=span,
        statistics=statistics,
        output_products=output_products,
        keep_input_datasets=keep_input_datasets,
    )
    return products
