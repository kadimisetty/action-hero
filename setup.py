from setuptools import find_packages, setup

from action_heroes.getters import get_about

import meta

about = get_about()

setup(
    name=about["PROJECT"]["program_name"],
    version=about["PROJECT"]["version"],
    description=about["PROJECT"]["description"],
    author=about["AUTHOR"]["name"],
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[
        "importlib_resources",
        "requests",
    ],
)
