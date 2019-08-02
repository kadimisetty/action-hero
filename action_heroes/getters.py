from configparser import ConfigParser, ExtendedInterpolation
import itertools
import pathlib

try:
    # importlib is available only from Python 3.7+
    from importlib import resources
except ImportError:
    # importlib_resources package is available for Python 3.4-3.6
    import importlib_resources as resources

import meta


def get_about():
    """Returns opened meta config file"""
    return get_config_as_dict(meta, "about.ini")


def get_readme_contents():
    """Return contents of file marked readme_filename in about.ini"""
    about = get_about()
    readme_filename = about["PROJECT"]["readme_filename"]
    with open("README.md", "r", encoding="utf-8") as f:
        readme_contents = f.read()

    return readme_contents


def get_readme_content_type():
    """Return content type of of file marked readme_filename in about.ini"""
    about = get_about()
    suffix = pathlib.Path(about["PROJECT"]["readme_filename"]).suffix

    if suffix is "md":
        return "text/markdown"
    elif suffix is "rst":
        return "text/x-rst"
    else:
        return "text/plain"


def get_config_as_dict(resource_path, config_filename):
    with resources.path(resource_path, config_filename) as config_path:
        config = ConfigParser(
            delimiters=("="),
            comment_prefixes=("#"),
            inline_comment_prefixes=("#"),
            interpolation=ExtendedInterpolation(),
        )
        config.read(config_path)
        return dict(config)
