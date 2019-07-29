import unittest
from argparse import ArgumentParser

from action_heroes.types import (
    IsConvertibleToIntAction,
    IsConvertibleToFloatAction,
    IsTruthyAction,
    IsFalsyAction,
)


class ParserEnclosedTestCase(unittest.TestCase):
    def setUp(self):
        """Setup new parser"""
        self.parser = ArgumentParser()


class TestIsConvertibleToIntAction(ParserEnclosedTestCase):
    def test_on_valid_value(self):
        self.parser.add_argument("--value", action=IsConvertibleToIntAction)
        value = "5"
        self.parser.parse_args(["--value", value])

    def test_on_valid_values_list(self):
        self.parser.add_argument(
            "--value", nargs="+", action=IsConvertibleToIntAction
        )
        values = ["100", "45", "99", "0"]
        self.parser.parse_args(["--value", *values])

    def test_on_invalid_value(self):
        self.parser.add_argument("--value", action=IsConvertibleToIntAction)
        value = "icecream"
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--value", value])

    def test_on_invalid_values_list(self):
        self.parser.add_argument(
            "--value", nargs="+", action=IsConvertibleToIntAction
        )
        values = ["puppy", "hanoi", "9.25", "X"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--value", *values])

    def test_on_mixed_valid_and_invalid_values_list(self):
        self.parser.add_argument(
            "--value", nargs="+", action=IsConvertibleToIntAction
        )
        values = ["4", "puppy", "hanoi", "9.25", "X", "12"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--value", *values])


class TestIsConvertibleToFloatAction(ParserEnclosedTestCase):
    def test_on_valid_value(self):
        self.parser.add_argument("--value", action=IsConvertibleToFloatAction)
        value = "5.3"
        self.parser.parse_args(["--value", value])

    def test_on_valid_values_list(self):
        self.parser.add_argument(
            "--value", nargs="+", action=IsConvertibleToFloatAction
        )
        values = ["100", "-4.3", "99", "0"]
        self.parser.parse_args(["--value", *values])

    def test_on_invalid_value(self):
        self.parser.add_argument("--value", action=IsConvertibleToFloatAction)
        value = "bunny"
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--value", value])

    def test_on_invalid_values_list(self):
        self.parser.add_argument(
            "--value", nargs="+", action=IsConvertibleToFloatAction
        )
        values = ["puppy", "hanoi", "9.25", "X"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--value", *values])

    def test_on_mixed_valid_and_invalid_values_list(self):
        self.parser.add_argument(
            "--value", nargs="+", action=IsConvertibleToFloatAction
        )
        values = ["4", "puppy", "hanoi", "9.25", "X", "12"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--value", *values])


class TestIsTruthyAction(ParserEnclosedTestCase):
    def test_on_truthy_value(self):
        self.parser.add_argument("--value", action=IsTruthyAction)
        value = "true"
        self.parser.parse_args(["--value", value])

    def test_on_truthy_values_list(self):
        self.parser.add_argument("--value", nargs="+", action=IsTruthyAction)
        values = ["true", "hundary"]
        self.parser.parse_args(["--value", *values])

    def test_on_falsy_value(self):
        self.parser.add_argument("--value", action=IsTruthyAction)
        value = ""
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--value", value])

    def test_on_falsy_values_list(self):
        self.parser.add_argument("--value", nargs="+", action=IsTruthyAction)
        values = ["", "0"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--value", *values])

    def test_on_mixed_truthy_and_falsy_values_list(self):
        self.parser.add_argument("--value", nargs="+", action=IsTruthyAction)
        values = ["", "0", "monday", "15"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--value", *values])
