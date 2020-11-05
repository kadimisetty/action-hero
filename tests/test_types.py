from action_hero.utils import ActionHeroTestCase
from action_hero import (
    IsConvertibleToFloatAction,
    IsConvertibleToIntAction,
    IsConvertibleToUUIDAction,
    IsFalsyAction,
    IsTruthyAction,
)


class TestIsConvertibleToIntAction(ActionHeroTestCase):
    def test_on_valid_value(self):
        """
        The test for validation.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--value", action=IsConvertibleToIntAction)
        value = "5"
        self.parser.parse_args(["--value", value])

    def test_on_valid_values_list(self):
        """
        This function to see if the test values.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--value", nargs="+", action=IsConvertibleToIntAction
        )
        values = ["100", "45", "99", "0"]
        self.parser.parse_args(["--value", *values])

    def test_on_invalid_value(self):
        """
        Set the argument.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--value", action=IsConvertibleToIntAction)
        value = "icecream"
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--value", value])

    def test_on_invalid_values_list(self):
        """
        Validate the test values.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--value", nargs="+", action=IsConvertibleToIntAction
        )
        values = ["puppy", "hanoi", "9.25", "X"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--value", *values])

    def test_on_mixed_valid_and_invalid_values_list(self):
        """
        This function for test values.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--value", nargs="+", action=IsConvertibleToIntAction
        )
        values = ["4", "puppy", "hanoi", "9.25", "X", "12"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--value", *values])


class TestIsConvertibleToFloatAction(ActionHeroTestCase):
    def test_on_valid_value(self):
        """
        Base validation for validation.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--value", action=IsConvertibleToFloatAction)
        value = "5.3"
        self.parser.parse_args(["--value", value])

    def test_on_valid_values_list(self):
        """
        Test if the test values.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--value", nargs="+", action=IsConvertibleToFloatAction
        )
        values = ["100", "-4.3", "99", "0"]
        self.parser.parse_args(["--value", *values])

    def test_on_invalid_value(self):
        """
        The test value isvalidator.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--value", action=IsConvertibleToFloatAction)
        value = "bunny"
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--value", value])

    def test_on_invalid_values_list(self):
        """
        This method to test for test values.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--value", nargs="+", action=IsConvertibleToFloatAction
        )
        values = ["puppy", "hanoi", "9.25", "X"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--value", *values])

    def test_on_mixed_valid_and_invalid_values_list(self):
        """
        Test if the test on the test.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--value", nargs="+", action=IsConvertibleToFloatAction
        )
        values = ["4", "puppy", "hanoi", "9.25", "X", "12"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--value", *values])


class TestIsTruthyAction(ActionHeroTestCase):
    def test_on_truthy_value(self):
        """
        Test for test value.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--value", action=IsTruthyAction)
        value = "true"
        self.parser.parse_args(["--value", value])

    def test_on_truthy_values_list(self):
        """
        Add test values todo test values.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--value", nargs="+", action=IsTruthyAction)
        values = ["true", "hundary"]
        self.parser.parse_args(["--value", *values])

    def test_on_falsy_value(self):
        """
        Test if fals.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--value", action=IsTruthyAction)
        value = ""
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--value", value])

    def test_on_falsy_values_list(self):
        """
        This function falsy values.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--value", nargs="+", action=IsTruthyAction)
        values = ["", "0"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--value", *values])

    def test_on_mixed_truthy_and_falsy_values_list(self):
        """
        Test if the test test values.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--value", nargs="+", action=IsTruthyAction)
        values = ["", "0", "monday", "15"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--value", *values])


class TestIsFalsyAction(ActionHeroTestCase):
    def test_on_truthy_value(self):
        """
        Test on test value.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--value", action=IsFalsyAction)
        value = "true"
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--value", value])

    def test_on_truthy_values_list(self):
        """
        Test if the test values.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--value", nargs="+", action=IsFalsyAction)
        values = ["true", "hundary"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--value", *values])

    def test_on_falsy_value(self):
        """
        Test if the test test for test test.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--value", action=IsFalsyAction)
        value = ""
        self.parser.parse_args(["--value", value])

    def test_on_falsy_values_list(self):
        """
        This function falsy - test test.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--value", nargs="+", action=IsFalsyAction)
        values = ["", "0"]
        self.parser.parse_args(["--value", *values])

    def test_on_mixed_truthy_and_falsy_values_list(self):
        """
        Test if the test values.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--value", nargs="+", action=IsFalsyAction)
        values = ["", "0", "monday", "15"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--value", *values])


class TestIsConvertibleToUUIDAction(ActionHeroTestCase):
    def test_on_valid_uuid_value(self):
        """
        Add a valid uuid value.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--value", action=IsConvertibleToUUIDAction)
        value = "cc3c3eb9-48a1-4307-8e92-700d9a25fffe"
        self.parser.parse_args(["--value", value])

    def test_on_valid_uppercase_uuid_value(self):
        """
        Test if the validation uuid is valid.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--value", action=IsConvertibleToUUIDAction)
        value = "CC3C3EB9-48A1-4307-8E92-700D9A25FFFE"
        self.parser.parse_args(["--value", value])

    def test_on_valid_mixedcase_uuid_value(self):
        """
        Test if the test value for a valid uuid.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--value", action=IsConvertibleToUUIDAction)
        value = "cC3C3Eb9-48a1-4307-8e92-700d9a25fFFE"
        self.parser.parse_args(["--value", value])

    def test_on_valid_uuid_values_list(self):
        """
        Validate a valid uuid is valid.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--value", nargs="+", action=IsConvertibleToUUIDAction
        )
        values = [
            "cc3c3eb9-48a1-4307-8e92-700d9a25fffe",
            "dfb55d07-340e-47e0-a3ba-0dc011369cef",
            "eca1f77c-e9c0-44c7-beeb-c8f7e0c59eb8",
        ]
        self.parser.parse_args(["--value", *values])

    def test_on_invalid_uuid_value(self):
        """
        Test that a uuid on a uuid.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--value", action=IsConvertibleToUUIDAction)
        value = ("spaghetti-monster-juice",)
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--value", value])

    def test_on_invalid_uuid_values_list(self):
        """
        This method is used tovalidate values are valid.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--value", nargs="+", action=IsConvertibleToUUIDAction
        )
        values = ["spaghetti-monster-juice", "", "--4-beeb-c8f7e0c59eb8"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--value", *values])

    def test_on_mixed_valid_and_invalid_values_list(self):
        """
        Test if the test values.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--value", nargs="+", action=IsConvertibleToUUIDAction
        )
        values = [
            "spaghetti-monster-juice",
            "cc3c3eb9-48a1-4307-8e92-700d9a25fffe",
            "",
            "dfb55d07-340e-47e0-a3ba-0dc011369cef",
            "--4-beeb-c8f7e0c59eb8",
        ]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--value", *values])

    def test_on_supported_uuid_forms(self):
        """
        Test if the supported supported values.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--value", nargs="+", action=IsConvertibleToUUIDAction
        )
        values = [
            "urn:uuid:12345678-1234-5678-1234-567812345678",
            "ca761232ed4211cebacd00aa0057b223",
            "CA761232-ED42-11CE-BACD-00AA0057B223",
            "{CA761232-ED42-11CE-BACD-00AA0057B223}",
        ]
        self.parser.parse_args(["--value", *values])

    def test_on_unsupported_uuid_forms(self):
        """
        Handle supported supported supported supported.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--value", nargs="+", action=IsConvertibleToUUIDAction
        )
        values = [
            "(CA761232-ED42-11CE-BACD-00AA0057B223)",
            "{}{}".format(
                "{0xCA761232, 0xED42, 0x11CE, {0xBA, 0xCD, ",
                "0x00, 0xAA, 0x00, 0x57, 0xB2, 0x23}}",
            ),
        ]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--value", *values])
