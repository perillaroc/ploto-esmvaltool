import typing

from esmvalcore._config import get_institutes, get_activity
from esmvalcore._recipe import _add_cmor_info
from esmvalcore.preprocessor._derive import get_required


def generate_variable(
        variable: typing.Dict,
        dataset: typing.Dict,
):
    v = combine_variable(
        variable=variable,
        dataset=dataset
    )
    add_variable_info(v)
    return v


def add_variable_info(
        variable: typing.Dict,
        override: bool=False
):
    _add_cmor_info(variable, override)

    if 'institute' not in variable:
        institute = get_institutes(variable)
        if institute:
            variable['institute'] = institute
    if 'activity' not in variable:
        activity = get_activity(variable)
        if activity:
            variable['activity'] = activity


def combine_variable(
        variable: typing.Dict,
        dataset: typing.Dict
):
    return {
        **variable,
        **dataset,
    }


def replace_variable_tag(
        item: str,
        variable: typing.Dict,
        **kwargs
) -> str:
    r = item.format(
        **variable,
        **kwargs
    )
    return r


def get_derive_input_variables(
        variable,
):
    required_variables = get_required(
        short_name=variable["short_name"],
        project=variable["project"]
    )

    def get_variable(v):
        r = {
            **variable,
            **v,
            "variable_group": f"{variable['short_name']}_derive_input_{v['short_name']}",
        }
        add_variable_info(r, override=True)
        return r

    # 输入变量
    input_variables = [get_variable(v) for v in required_variables]
    return input_variables

