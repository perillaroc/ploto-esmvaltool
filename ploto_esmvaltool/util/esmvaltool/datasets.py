import typing


INFO_KEYS = (
    'project',
    'activity',
    'dataset',
    'exp',
    'ensemble',
    'version'
)


def set_alias(
        datasets:typing.Dict
):
    """
    see esmvalcore._recipe.Recipe.set_alias method.
    """
    datasets_info = set()

    def _key_str(obj):
        if isinstance(obj, str):
            return obj
        try:
            return '-'.join(obj)
        except TypeError:
            return str(obj)

    for variable in datasets.values():
        for dataset in variable:
            alias = tuple(
                _key_str(dataset.get(key, None)) for key in INFO_KEYS)
            datasets_info.add(alias)
            if 'alias' not in dataset:
                dataset['alias'] = alias

    alias = dict()
    for info in datasets_info:
        alias[info] = []

    datasets_info = list(datasets_info)
    _get_next_alias(alias, datasets_info, 0)

    for info in datasets_info:
        alias[info] = '_'.join(
            [str(value) for value in alias[info] if value is not None])
        if not alias[info]:
            alias[info] = info[INFO_KEYS.index('dataset')]

    for variable in datasets.values():
        for dataset in variable:
            dataset['alias'] = alias.get(dataset['alias'],
                                         dataset['alias'])


def _get_next_alias(alias, datasets_info, i):
    """
    see esmvalcore._recipe.Recipe._get_next_alias method.
    """
    if i >= len(INFO_KEYS):
        return
    key_values = set(info[i] for info in datasets_info)
    if len(key_values) == 1:
        for info in iter(datasets_info):
            alias[info].append(None)
    else:
        for info in datasets_info:
            alias[info].append(info[i])
    for key in key_values:
        _get_next_alias(
            alias,
            [info for info in datasets_info if info[i] == key],
            i + 1,
        )
