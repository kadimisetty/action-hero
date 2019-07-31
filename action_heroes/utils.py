import unittest
import functools
import argparse

import requests


__all__ = [
    "MapAction",
    "CheckAction",
    "ParserEnclosedTestCase",
    "run_only_when_when_internet_is_up",
]


def run_only_when_when_internet_is_up(urls=["http://www.google.com"]):
    """Decorator that runs wrapped function when the internet is up.

    Note:
        - Connection is checked by checking connecrion to values in urls

    """

    def run_only_when_when_internet_is_up_wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Do network check
            try:
                [requests.get(url).raise_for_status() for url in urls]

                func(*args, **kwargs)

            # Do nothing on response error
            except requests.exceptions.RequestException:
                pass

        return wrapper

    return run_only_when_when_internet_is_up_wrapper


class ParserEnclosedTestCase(unittest.TestCase):
    """unitests.TestCase subclass that encloses an argparser instance"""

    def setUp(self):
        """Enclose argparser.ArgumentParser inside setUp"""
        self.parser = argparse.ArgumentParser()


class BaseAction(argparse.Action):
    """ArgumentParser Action subclass that runs user's func over values"""

    func = None
    err_msg_singular = None
    err_msg_plural = None

    @classmethod
    def run_user_func(cls, value):
        return cls.func(value)

    def __init__(
        self, option_strings, dest, nargs=None, help=None, metavar=None
    ):
        if not self.func:
            raise ValueError("func is required")
        elif not self.err_msg_singular:
            raise ValueError("func is required")
        if not self.err_msg_plural:
            raise ValueError("func is required")

        super(BaseAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            help=help,
            metavar=metavar,
        )


class CheckAction(BaseAction):
    def __call__(self, parser, namespace, values, option_string=None):
        # When values are a list of strings
        if isinstance(values, list):
            if False in [self.run_user_func(value) for value in values]:
                raise ValueError(self.err_msg_plural)

        # When values is one string
        else:
            value = values
            if not self.run_user_func(value):
                raise ValueError(self.err_msg_singular)

        setattr(namespace, self.dest, values)


class MapAction(BaseAction):
    def __call__(self, parser, namespace, values, option_string=None):
        # When values are a list of strings
        if isinstance(values, list):
            [self.run_user_func(value) for value in values]

        # When values is one string
        else:
            value = values
            self.run_user_func(value)

        setattr(namespace, self.dest, values)
