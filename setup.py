from setuptools import find_packages, setup

from action_heroes.getters import get_about


about = get_about()

setup(
    name=about["PROJECT"]["program_name"],
    version=about["PROJECT"]["version"],
    description=about["PROJECT"]["description"],
    author=about["AUTHOR"]["name"],
    author_email=about["AUTHOR"]["email"],
    python_requires=">={}".format(about["PROJECT"]["requires_python"]),
    url=about["PROJECT"]["url"],
    license=about["PROJECT"]["license"],
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=["importlib_resources", "requests"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Terminals",
    ],
)
