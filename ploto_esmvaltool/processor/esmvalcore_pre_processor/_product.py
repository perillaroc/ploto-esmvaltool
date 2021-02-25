from pathlib import Path


def _update_product_output(
        product,
        output,
):
    product = product.copy()
    product_output = product["output"]
    output_directory = output.get("output_directory", "")
    product_output_directory = product_output.get("output_directory", "")
    output_directory = str(Path(
        output_directory,
        product_output_directory
    ))

    product_output["output_directory"] = output_directory
    return product


def _add_diagnostic(
        product,
        diagnostic,
):
    product["variable"] = {
        **product["variable"],
        **diagnostic,
    }
    return product
