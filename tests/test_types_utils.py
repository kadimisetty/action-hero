import unittest

from action_heroes.types_utils import (
    is_convertible_to_int,
    is_convertible_to_float,
    is_truthy,
)


class TestIsConvertibleToInt(unittest.TestCase):
    def test_on_valid_value_zero(self):
        value = "0"
        self.assertTrue(is_convertible_to_int(value))

    def test_on_valid_value_positive_integer(self):
        value = "3"
        self.assertTrue(is_convertible_to_int(value))

    def test_on_valid_value_negative_integer(self):
        value = "-20"
        self.assertTrue(is_convertible_to_int(value))

    def test_on_invalid_value_string(self):
        value = "banana"
        self.assertFalse(is_convertible_to_int(value))

    def test_on_invalid_value_float(self):
        value = "3.40"
        self.assertFalse(is_convertible_to_int(value))

    def test_on_invalid_value_blank(self):
        value = ""
        self.assertFalse(is_convertible_to_int(value))


class TestIsConvertibleToFloat(unittest.TestCase):
    def test_on_valid_value_zero(self):
        value = "0"
        self.assertTrue(is_convertible_to_float(value))

    def test_on_valid_value_positive_integer(self):
        value = "3"
        self.assertTrue(is_convertible_to_float(value))

    def test_on_valid_value_negative_integer(self):
        value = "-20"
        self.assertTrue(is_convertible_to_float(value))

    def test_on_valid_value_positive_float(self):
        value = "234.5"
        self.assertTrue(is_convertible_to_float(value))

    def test_on_valid_value_negative_float(self):
        value = "-20.123"
        self.assertTrue(is_convertible_to_float(value))

    def test_on_invalid_value_string(self):
        value = "banana"
        self.assertFalse(is_convertible_to_float(value))

    def test_on_invalid_value_blank(self):
        value = ""
        self.assertFalse(is_convertible_to_float(value))


class TestIsTruthy(unittest.TestCase):
    def test_on_truthy_value_strings(self):
        value = "true"
        self.assertTrue(is_truthy(value))

    def test_on_falsy_value_strings_blank(self):
        value = ""
        self.assertFalse(is_truthy(value))

    def test_on_falsy_value_floats_zeroes_list(self):
        values = ["0", "0.0"]
        [self.assertFalse(is_truthy(value)) for value in values]
