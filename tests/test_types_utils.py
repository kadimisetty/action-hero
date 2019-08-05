import unittest

from action_hero.types_utils import (
    is_convertible_to_UUID,
    is_convertible_to_float,
    is_convertible_to_int,
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


class TestIsConvertibleToUUID(unittest.TestCase):
    def test_on_valid_UUID_value(self):
        value = "9cc79eb2-ed8a-4216-b1a8-9ab65bc4d92b"
        self.assertTrue(is_convertible_to_UUID(value))

    def test_on_valid_UUID_values_list(self):
        values = [
            "9cc79eb2-ed8a-4216-b1a8-9ab65bc4d92b",
            "16fd2706-8baf-433b-82eb-8c7fada847da",
            "527e620b-180d-49d0-9811-8c4e0aa7f095",
        ]
        [self.assertTrue(is_convertible_to_UUID(value)) for value in values]

    def test_on_invalid_UUID_value(self):
        value = "monday-tuesday-wednesday-thursday-friday-saturday-sunday"
        self.assertFalse(is_convertible_to_UUID(value))

    def test_on_invalid_UUID_values_list(self):
        values = ["chocolate-pudding", "231", "002345234"]
        self.assertIn(False, [is_convertible_to_UUID(v) for v in values])

    def test_on_mixed_valid_and_invalid_UUID_values_list(self):

        values = [
            "9cc79eb2-ed8a-4216-b1a8-9ab65bc4d92b",
            "chocolate-pudding",
            "16fd2706-8baf-433b-82eb-8c7fada847da",
            "231",
            "527e620b-180d-49d0-9811-8c4e0aa7f095",
            "002345234",
        ]
        self.assertIn(False, [is_convertible_to_UUID(v) for v in values])
