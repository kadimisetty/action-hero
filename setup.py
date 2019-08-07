from setuptools import find_packages, setup
import pathlib


AUTHOR = "Sri Kadimisetty"
AUTHOR_EMAIL = "s@sri.io"

PROGRAM_NAME = "action-hero"
PROGRAM_VERSION = "0.6.3"
DESCRIPTION = "Argparse Actions that pack a punch!"
URL = "https://github.com/kadimisetty/action-hero"
LICENSE = "MIT"
PYTHON_REQUIREMENTS = ">=3.5.0"


def get_long_description(file="README.md"):
    """Return contents of long description from contents of file"""
    with open(file, "r", encoding="utf-8") as f:
        return f.read()


def get_long_description_content_type(file="README.md"):
    """Return content-type of long description from content-type of file"""
    suffix = pathlib.Path(file).suffix
    content_types = {"md": "text/markdown", "rst": "text/x-rst"}
    return content_types.get(suffix, "text/plain")


setup(
    name=PROGRAM_NAME,
    version=PROGRAM_VERSION,
    description=DESCRIPTION,
    long_description=get_long_description(),
    long_description_content_type=get_long_description_content_type(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    python_requires=PYTHON_REQUIREMENTS,
    url=URL,
    license=LICENSE,
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=["requests"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Terminals",
        "Natural Language :: English",
    ],
)
