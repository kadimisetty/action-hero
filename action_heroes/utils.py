import unittest
import functools
import argparse

import requests


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
