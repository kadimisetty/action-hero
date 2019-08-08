import unittest

from action_hero.utils import ActionHeroTestCase, capture_output
from action_hero import (
    ChoicesAction,
    ConfirmAction,
    NotifyAndContinueAction,
    NotifyAndExitAction,
)


class TestChoicesAction(ActionHeroTestCase):
    def test_on_adding_to_parser(self):
        self.parser.add_argument(
            "--color", action=ChoicesAction, action_values=["black", "white"]
        )

    def test_on_absent_action_values(self):
        with self.assertRaises(ValueError):
            self.parser.add_argument("--color", action=ChoicesAction)

    def test_on_blank_action_values(self):
        with self.assertRaises(ValueError):
            self.parser.add_argument("--color", action=ChoicesAction)

    def test_on_matching_choice_to_action_values(self):
        self.parser.add_argument(
            "--number", action=ChoicesAction, action_values=["one", "two"]
        )
        self.parser.parse_args(["--number", "one"])

    def test_on_nonmatching_choice_to_action_values(self):
        self.parser.add_argument(
            "--number", action=ChoicesAction, action_values=["one", "two"]
        )
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--number", "three"])


class TestNotifyAndContinueAction(ActionHeroTestCase):
    def test_on_adding_to_parser(self):
        self.parser.add_argument(
            "--message",
            action=NotifyAndContinueAction,
            action_values=["hello"],
        )

    def test_on_accepting_single_message(self):
        self.parser.add_argument(
            "--message",
            action=NotifyAndContinueAction,
            action_values=["hello"],
        )

    def test_on_accepting_multiple_messages(self):
        self.parser.add_argument(
            "--message",
            action=NotifyAndContinueAction,
            action_values=["hello", "hello again", "hello, yet, again"],
        )

    def test_on_not_quitting_after_displaying_message(self):
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
        self.parser.add_argument(
            "--message", action=NotifyAndExitAction, action_values=["hello"]
        )

    def test_on_accepting_single_message(self):
        self.parser.add_argument(
            "--message", action=NotifyAndExitAction, action_values=["hello"]
        )

    def test_on_accepting_multiple_messages(self):
        self.parser.add_argument(
            "--message",
            action=NotifyAndExitAction,
            action_values=["hello", "hello again", "hello, yet, again"],
        )

    def test_on_quitting_after_displaying_message(self):
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


@unittest.skip("not implemented")
class TestConfirmAction(ActionHeroTestCase):
    def test_on_adding_to_parser(self):
        self.parser.add_argument(
            "--message", action=ConfirmAction, action_values=["black", "white"]
        )
