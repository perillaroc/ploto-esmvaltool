import typing

from esmvalcore._recipe import _add_cmor_info


def add_variable_info(variable: typing.Dict, override: bool=False):
    _add_cmor_info(variable, override)


def combine_variable(variable: typing.Dict, dataset: typing.Dict):
    return {
        **variable,
        **dataset,
    }


def replace_variable_tag(item: str, variable: typing.Dict) -> str:
    r = item.format(**variable)
    return r