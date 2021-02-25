import typing

from esmvalcore._recipe import _add_cmor_info
from esmvalcore._config import (
    get_institutes,
    get_activity,
)


def add_variable_info(variable: typing.Dict, override: bool=False):
    _add_cmor_info(variable, override)

    if 'institute' not in variable:
        institute = get_institutes(variable)
        if institute:
            variable['institute'] = institute
    if 'activity' not in variable:
        activity = get_activity(variable)
        if activity:
            variable['activity'] = activity


def combine_variable(variable: typing.Dict, dataset: typing.Dict):
    return {
        **variable,
        **dataset,
    }


def replace_variable_tag(item: str, variable: typing.Dict) -> str:
    r = item.format(**variable)
    return r