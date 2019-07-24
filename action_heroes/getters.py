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
