import unittest
from unittest import mock

from action_hero.utils import ActionHeroTestCase, capture_output
from action_hero import (
    ChoicesAction,
    ConfirmAction,
    NotifyAndContinueAction,
    NotifyAndExitAction,
)


class TestChoicesAction(ActionHeroTestCase):
    def test_on_adding_to_parser(self):
        """
        Register the test test results to test.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--color", action=ChoicesAction, action_values=["black", "white"]
        )

    def test_on_absent_action_values(self):
        """
        Set the action action action.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(ValueError):
            self.parser.add_argument("--color", action=ChoicesAction)

    def test_on_blank_action_values(self):
        """
        Sets the action action.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(ValueError):
            self.parser.add_argument("--color", action=ChoicesAction)

    def test_on_matching_choice_to_action_values(self):
        """
        Add action action to action_values.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--number", action=ChoicesAction, action_values=["one", "two"]
        )
        self.parser.parse_args(["--number", "one"])

    def test_on_nonmatching_choice_to_action_values(self):
        """
        Test that action to action to action. action.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--number", action=ChoicesAction, action_values=["one", "two"]
        )
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--number", "three"])


class TestNotifyAndContinueAction(ActionHeroTestCase):
    def test_on_adding_to_parser(self):
        """
        Sets the test command.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--message",
            action=NotifyAndContinueAction,
            action_values=["hello"],
        )

    def test_on_accepting_single_message(self):
        """
        The test message received when the test is received.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--message",
            action=NotifyAndContinueAction,
            action_values=["hello"],
        )

    def test_on_accepting_multiple_messages(self):
        """
        This method for test test.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--message",
            action=NotifyAndContinueAction,
            action_values=["hello", "hello again", "hello, yet, again"],
        )

    def test_on_not_quitting_after_displaying_message(self):
        """
        Test if the test is scheduled.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--message",
            nargs=0,
            action=NotifyAndContinueAction,
            action_values=["hello"],
        )
        self.assertEqual(
            capture_output(self.parser.parse_args, ["--message"]), "hello"
        )

    def test_on_not_quitting_after_displaying_multiple_messages(self):
        """
        Test if the test is received.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--message",
            nargs=0,
            action=NotifyAndContinueAction,
            action_values=["hello", "ola", "salve"],
        )

        self.assertEqual(
            capture_output(self.parser.parse_args, ["--message"]),
            "hello\nola\nsalve",
        )


class TestNotifyAndExitAction(ActionHeroTestCase):
    def test_on_adding_to_parser(self):
        """
        Register the test test command.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--message",
            action=NotifyAndExitAction,
            action_values=["hello"],
            nargs=0,
        )

    def test_on_accepting_single_message(self):
        """
        The test message received from the test.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--message",
            action=NotifyAndExitAction,
            action_values=["hello"],
            nargs=0,
        )

    def test_on_accepting_multiple_messages(self):
        """
        The test test test for test test.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--message",
            action=NotifyAndExitAction,
            nargs=0,
            action_values=["hello", "hello again", "hello, yet, again"],
        )

    def test_on_quitting_after_displaying_message(self):
        """
        Test if the on_on_message is received.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--message",
            nargs=0,
            action=NotifyAndExitAction,
            action_values=["hello"],
        )
        with self.assertRaises(SystemExit):
            # Capturing output to prevent polluting test report
            capture_output(self.parser.parse_args, ["--message"])

    def test_on_quitting_after_displaying_multiple_messages(self):
        """
        Captures on - quitting on_on_multiple_on_display.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--message",
            nargs=0,
            action=NotifyAndExitAction,
            action_values=["hello", "ola", "salve"],
        )

        with self.assertRaises(SystemExit):
            # Capturing output to prevent polluting test report
            capture_output(self.parser.parse_args, ["--message"])

    @unittest.skip("not implemented -- TODO return val before exit")
    def test_on_getting_expectied_message_after_displaying_message(self):
        """
        The on_on_expectied.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--message",
            nargs=0,
            action=NotifyAndExitAction,
            action_values=["hello"],
        )

        result = None
        try:
            # Capturing output to prevent polluting test report
            result = capture_output(self.parser.parse_args, ["--message"])

        except SystemExit:
            self.assertEqual(result, "hello")

    @unittest.skip("not implemented -- TODO return val before exit")
    def test_on_getting_expected_messages_after_displaying_multiple_messages(
        self
    ):
        """
        Captures on_on_on_on_getting_getting_messages_messages_messages_messages

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--message",
            nargs=0,
            action=NotifyAndExitAction,
            action_values=["hello", "ola", "salve"],
        )

        result = None
        try:
            # Capturing output to prevent polluting test report
            result = capture_output(self.parser.parse_args, ["--message"])

        except SystemExit:
            self.assertEqual(result, "hello\nola\nsalve")


class TestConfirmAction(ActionHeroTestCase):
    def test_on_adding_to_parser_with_nargs_implicit(self):
        """
        Register the test test results to test when the test.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--message", action=ConfirmAction, action_values=["casablanca"]
        )

    def test_on_adding_to_parser_with_nargs_explicit(self):
        """
        Register the argument parser for the test the argument parser.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--message",
            action=ConfirmAction,
            nargs=0,
            action_values=["Continue?"],
        )

    def test_on_accepting_single_message(self):
        """
        The callback for the test.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--message",
            action=ConfirmAction,
            nargs=0,
            action_values=["Continue?"],
        )

    def test_on_accepting_multiple_messages(self):
        """
        This method is called when the test is received.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--message",
            action=ConfirmAction,
            nargs=0,
            action_values=["Failed Install", "Try Again?"],
        )

    def test_on_not_quitting_on_y(self):
        """
        Test if the test test test.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--message",
            action=ConfirmAction,
            nargs=0,
            action_values=["Continue?"],
        )
        # No SystemExit on "y"
        with mock.patch('builtins.input', return_value="y"):
            self.parser.parse_args(["--message"])

    def test_on_quitting_on_n(self):
        """
        The on on on on on on on on the test.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--message",
            action=ConfirmAction,
            nargs=0,
            action_values=["Continue?"],
        )
        # Assert SystemExit on not n
        with self.assertRaises(SystemExit):
            with mock.patch('builtins.input', return_value="n"):
                self.parser.parse_args(["--message"])

    @unittest.skip("TODO capture stdout and mock input")
    def test_on_displaying_message_and_not_quit_on_y(self):
        """
        Disables on_on_y.

        Args:
            self: (todo): write your description
        """
        raise NotImplementedError

    @unittest.skip("TODO capture stdout and mock input")
    def test_on_displaying_multiple_messages_and_not_quit_on_y(self):
        """
        !

        Args:
            self: (todo): write your description
        """
        raise NotImplementedError

    @unittest.skip("TODO capture stdout and mock input")
    def test_on_displaying_message_and_quit_on_n(self):
        """
        Set the test_on_on_on_display.

        Args:
            self: (todo): write your description
        """
        raise NotImplementedError

    @unittest.skip("TODO capture stdout and mock input")
    def test_on_displaying_multiple_messages_and_quit_on_n(self):
        """
        Set the default is_on_on_multiple_multiple_quit.

        Args:
            self: (todo): write your description
        """
        raise NotImplementedError
