# coding=utf-8
from setuptools import setup, find_packages
import io
import re

with io.open("ploto_esmvaltool/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name='ploto-esmvaltool',

    version=version,

    description='Ploto-esmvaltool project.',
    long_description=__doc__,

    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),

    include_package_data=True,

    package_data={
        '': ['*.ncl'],
    },

    zip_safe=False,

    install_requires=[
        "attrs",
        "click",
        "pyyaml",
        "loguru",
        "esmvalcore",
    ],

    extras_require={
        'test': [],
    }
)