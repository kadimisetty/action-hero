import unittest
import argparse


from action_heroes.utils import ParserEnclosedTestCase


class TestParserEnclosedTestCase(ParserEnclosedTestCase):
    def test_argparse_argument_parser_is_present(self):
        self.assertTrue(hasattr(self, "parser"))

    def test_argparse_argument_parser_is_of_correct_type(self):
        self.assertIsInstance(self.parser, argparse.ArgumentParser)

    def test_is_subclassed_from_unittest_testcase(self):
        self.assertTrue(issubclass(ParserEnclosedTestCase, unittest.TestCase))
