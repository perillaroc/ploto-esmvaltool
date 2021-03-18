import typing

from .variable import generate_variables


INFO_KEYS = (
    'project',
    'activity',
    'dataset',
    'exp',
    'ensemble',
    'version'
)


def get_datasets(
        variables: typing.List,
        datasets: typing.List = None,
        variable_additional_datasets: typing.Optional[typing.Dict] = None,
        additional_datasets: typing.Optional[typing.Dict] = None
) -> typing.Dict:
    """

    Parameters
    ----------
    datasets: typing.List
        From recipe datasets.
        [
            {
                "dataset": "FGOALS-g3",
                "grid": "gn"
            },
            {
                "dataset": "NESM3",
                "grid": "gn"
            },
        ]
    variables: typing.List
        From recipe variables.
        [
            {
                "variable_group": "tas",
                "short_name": "tas",

                "preprocessor": "clim_ref",
                "reference_dataset": "HadCRUT4",

                "project": "CMIP6",
                "mip": "Amon",
                "exp": "historical",
                "ensemble": "r1i1p1f1",
                "frequency": "mon",

                "start_year": 1850,
                "end_year": 2014
            }
        ]
    variable_additional_datasets: typing.Dict
        A dictionary with variable_group as key.
        From recipe additional_datasets.
        {
            "tas": [
                {
                    "dataset": "HadCRUT4",
                    "project": "OBS",
                    "type": "ground",
                    "version": "1",
                    "tier": 2,
                    "end_year": 2017,
                }
            ],
        }
    additional_datasets: typing.Dict

    Returns
    -------
    typing.Dict
        {
            "tas": [
                {
                    # combined_variable with alias and index

                    "alias": "...",
                    "recipe_dataset_index": 0,  # 1, 2, 3, ...
                }
            ]
        }
    """
    ds = {}
    if datasets is None:
        datasets = []
    if variable_additional_datasets is None:
        variable_additional_datasets = []
    if additional_datasets is None:
        additional_datasets = []

    for variable in variables:
        group_variables = []
        if variable["variable_group"] in variable_additional_datasets:
            v_additional_datasets = variable_additional_datasets[variable["variable_group"]]
        else:
            v_additional_datasets = []
        recipe_dataset_index = 0
        for d in [
            *datasets,
            *v_additional_datasets,
            *additional_datasets
        ]:
            vs = generate_variables(
                variable=variable,
                dataset=d,
            )
            for v in vs:
                v["recipe_dataset_index"] = recipe_dataset_index
                recipe_dataset_index += 1
                group_variables.append(v)
        ds[variable["variable_group"]] = group_variables

    set_alias(ds)

    return ds


def set_alias(
        datasets: typing.Dict
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

    for variables in datasets.values():
        for dataset in variables:
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
