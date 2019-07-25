import unittest
from argparse import ArgumentParser
from argparse import ArgumentTypeError


class TestCaseWithParser(unittest.TestCase):
    def setUp(self):
        """Setup new parser"""
        self.parser = ArgumentParser()


class TestResolvePathAction(TestCaseWithParser):
    pass
