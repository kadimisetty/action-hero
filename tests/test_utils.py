import argparse
import os
import tempfile
import unittest

from action_hero.utils import (
    ActionHeroAction,
    ActionHeroTestCase,
    BaseAction,
    CheckAction,
    CheckPresentInValuesAction,
    DisplayMessageAndExitAction,
    ExitCapturedArgumentParser,
    MapAction,
    MapAndReplaceAction,
    PipelineAction,
    run_only_when_modules_loaded,
    run_only_when_when_internet_is_up,
)
from action_hero import (
    FileExistsAction,
    FileIsEmptyAction,
    FileIsWritableAction,
)


class TestRunOnlyWhenWhenInternetIsUp(ActionHeroTestCase):
    def test_on_reachable_url(self):
        """
        Test if the given url is on the given test.

        Args:
            self: (todo): write your description
        """
        @run_only_when_when_internet_is_up(urls="AAA")
        def func():
            """
            Decorator function that takes a list of the given value.

            Args:
            """
            raise ValueError

        # Should not run this func since the url is invalid and unreachable
        func()


class TestRunOnlyWhenModuleLoaded(unittest.TestCase):
    def test_on_available_module_unittest(self):
        """
        Sets the module that the given modules.

        Args:
            self: (todo): write your description
        """
        @run_only_when_modules_loaded(modules=["sys"])
        def raise_value_error():
            """
            Raises an error.

            Args:
            """
            raise ValueError()

        # Assert that func raise_value_error runs
        with self.assertRaises(ValueError):
            raise_value_error()

    def test_on_unavailable_module_unittest(self):
        """
        Triggered modules that have been loaded.

        Args:
            self: (todo): write your description
        """
        @run_only_when_modules_loaded(modules=["unavailable_module_xyz"])
        def raise_value_error():
            """
            Raises an error.

            Args:
            """
            raise ValueError()

        # func raise_value_error does not run
        raise_value_error()


class TestActionHeroTestCase(ActionHeroTestCase):
    def test_argparse_argument_parser_is_present(self):
        """
        Check if the argument is a test argument.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(hasattr(self, "parser"))

    def test_argparse_argument_parser_is_instance_of_argument_parser(self):
        """
        Check if argument parser.

        Args:
            self: (todo): write your description
        """
        self.assertIsInstance(self.parser, argparse.ArgumentParser)

    def test_argparse_argument_parser_is_instance_of_custom_parser(self):
        """
        Utility method argparse. argparse.

        Args:
            self: (todo): write your description
        """
        self.assertIsInstance(self.parser, ExitCapturedArgumentParser)

    def test_is_subclassed_of_unittest_testcase(self):
        """
        Tests if the given testcase is a test.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(issubclass(ActionHeroTestCase, unittest.TestCase))


class TestBaseAction(ActionHeroTestCase):
    def test_if_proper_subclass(self):
        """
        Assert that the test is a test.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(issubclass(BaseAction, argparse.Action))


class TestCheckAction(ActionHeroTestCase):
    def test_if_proper_subclass(self):
        """
        Assert that the test class.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(issubclass(CheckAction, argparse.Action))

    def test_if_checks_for_required_func(self):
        """
        Check if the required checksum of the test.

        Args:
            self: (todo): write your description
        """
        class CheckActionWithotFunc(CheckAction):
            error_message = "E"

        with self.assertRaises(ValueError):
            CheckActionWithotFunc(option_strings=[], dest="")

    def test_if_checks_for_required_error_message(self):
        """
        Raise the message for the expected to raise an error.

        Args:
            self: (todo): write your description
        """
        class CheckActionWithotErrorMessage(CheckAction):
            func = print

        with self.assertRaises(ValueError):
            CheckActionWithotErrorMessage(option_strings=[], dest="")


class TestMapAction(ActionHeroTestCase):
    def test_if_proper_subclass(self):
        """
        Assert that the test is a test. argparse class.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(issubclass(MapAction, argparse.Action))

    def test_if_checks_for_required_func(self):
        """
        Check if the required checksum of the test.

        Args:
            self: (todo): write your description
        """
        class MapActionWithotFunc(MapAction):
            pass

        with self.assertRaises(ValueError):
            MapActionWithotFunc(option_strings=[], dest="")


class TestMapAndReplaceAction(ActionHeroTestCase):
    def test_if_proper_subclass(self):
        """
        Assigns the test class to the given test.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(issubclass(MapAndReplaceAction, argparse.Action))

    def test_if_checks_for_required_func(self):
        """
        Assigns the required checksum of the argument.

        Args:
            self: (todo): write your description
        """
        class MapAndReplaceWithotFunc(MapAndReplaceAction):
            pass

        with self.assertRaises(ValueError):
            MapAndReplaceWithotFunc(option_strings=[], dest="")


class TestCheckPresentInValuesAction(ActionHeroTestCase):
    def test_on_subclass_of_argparse_action(self):
        """
        Assigns the argparse argument.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(
            issubclass(CheckPresentInValuesAction, argparse.Action)
        )

    def test_on_action_value_that_is_not_a_list(self):
        """
        Test if action.

        Args:
            self: (todo): write your description
        """
        class Action1(CheckPresentInValuesAction):
            def func(value):
                """
                Decorator to wrap a function.

                Args:
                    value: (todo): write your description
                """
                return value

            error_message = "E"

        with self.assertRaises(ValueError):
            self.parser.add_argument(
                "--number", action=Action1, action_values=()
            )

    def test_on_empty_action_values(self):
        """
        Decor function that action is empty.

        Args:
            self: (todo): write your description
        """
        class Action1(CheckPresentInValuesAction):
            def func(value):
                """
                Decorator to wrap a function.

                Args:
                    value: (todo): write your description
                """
                return value

            error_message = "E"

        with self.assertRaises(ValueError):
            self.parser.add_argument(
                "--number", action=Action1, action_values=[]
            )

    def test_on__required_func_and_err_msgs(self):
        """
        Decor for required error occurs.

        Args:
            self: (todo): write your description
        """
        class Action1(CheckPresentInValuesAction):
            pass

        with self.assertRaises(ValueError):
            Action1(option_strings=[], dest="", action_values=["UV"])

    def test_on_required_value(self):
        """
        The test value of the test.

        Args:
            self: (todo): write your description
        """
        class Action1(CheckPresentInValuesAction):
            def func(value):
                """
                Decorator to wrap a function.

                Args:
                    value: (todo): write your description
                """
                return value

            error_message = "E"

        with self.assertRaises(ValueError):
            Action1(option_strings=[], dest="")

    def test_on_action_values_with_uneven_types(self):
        """
        Test if the given value should be received.

        Args:
            self: (todo): write your description
        """
        class Action1(CheckPresentInValuesAction):
            def func(value):
                """
                Decorator to wrap a function.

                Args:
                    value: (todo): write your description
                """
                return value

            error_message = "E"

        with self.assertRaises(ValueError):
            self.parser.add_argument(
                "--color", action=Action1, action_values=["red", "blue", 2]
            )

    def test_on_action_values_with_type_specified(self):
        """
        Decorator for the given a test value.

        Args:
            self: (todo): write your description
        """
        class Action1(CheckPresentInValuesAction):
            def func(value):
                """
                Decorator to wrap a function.

                Args:
                    value: (todo): write your description
                """
                return value

            error_message = "E"

        self.parser.add_argument(
            "--number", action=Action1, type=int, action_values=[1, 2, 3]
        )

        self.parser.parse_args(["--number", "2"])

    def test_on_action_values_with_unheeded_type_specified(self):
        """
        Test if the value of the given value.

        Args:
            self: (todo): write your description
        """
        class Action1(CheckPresentInValuesAction):
            def func(value):
                """
                Decorator to wrap a function.

                Args:
                    value: (todo): write your description
                """
                return value

            error_message = "E"

        self.parser.add_argument(
            "--number", action=Action1, action_values=[4, 5, 6]
        )

        with self.assertRaises(ValueError):
            self.parser.parse_args(["--number", "5"])

    def test_on_action_values_with_mixed_type_specified(self):
        """
        The test action action.

        Args:
            self: (todo): write your description
        """
        class Action1(CheckPresentInValuesAction):
            def func(value):
                """
                Decorator to wrap a function.

                Args:
                    value: (todo): write your description
                """
                return value

            error_message = "E"

        with self.assertRaises(ValueError):
            self.parser.add_argument(
                "--number", action=Action1, action_values=[4, 5, "6"]
            )

    def test_on_uncastable_action_value_entry(self):
        """
        The uncast a test value.

        Args:
            self: (todo): write your description
        """
        class Action1(CheckPresentInValuesAction):
            def func(value):
                """
                Decorator to wrap a function.

                Args:
                    value: (todo): write your description
                """
                return value

            error_message = "E"

        self.parser.add_argument(
            "--number", action=Action1, action_values=["four"], type=int
        )

        with self.assertRaises(ValueError):
            self.parser.parse_args(["--number", "4"])


class TestActionHeroAction(ActionHeroTestCase):
    def test_if_proper_subclass(self):
        """
        Assigns a test is a subclass.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(issubclass(ActionHeroAction, argparse.Action))


class TestPipelineAction(ActionHeroTestCase):
    """Known issue with testing PipelineActions using actions w/ action_values
    tends to cause errors where some test cases do not have any content for
    values"""

    def test_if_is_subclass_of_actionheroaction(self):
        """
        Assigns the given action to the given action.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(issubclass(PipelineAction, ActionHeroAction))

    def test_on_child_action(self):
        """
        Test if a child file to be run.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--file", action=PipelineAction, action_values=[FileExistsAction]
        )
        file1 = tempfile.mkstemp()[1]
        self.parser.parse_args(["--file", file1])
        os.remove(file1)

        # file1 now doesn't exist
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--file", file1])

    def test_on_empty_list_of_child_actions(self):
        """
        Add empty empty when the child elements.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(ValueError):
            self.parser.add_argument(
                "--file", action=PipelineAction, action_values=[]
            )

    def test_on_action_value_of_wrong_type_int(self):
        """
        The callback for setting the arguments to action.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(ValueError):
            self.parser.add_argument(
                "--file", action=PipelineAction, action_values=5
            )

    def test_on_action_value_of_wrong_type_str(self):
        """
        The callback for setting up to the value of the action.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(ValueError):
            self.parser.add_argument(
                "--file", action=PipelineAction, action_values=5
            )

    def test_on_action_value_of_wrong_type_action_with_no_list(self):
        """
        Assigns_on_action_action_action_action_action_action_action_action_action_action.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(ValueError):
            self.parser.add_argument(
                "--file", action=PipelineAction, action_values=FileExistsAction
            )

    def test_on_list_of_child_multiple_actions(self):
        """
        Create a file - like file to - like object

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--file",
            action=PipelineAction,
            action_values=[
                FileExistsAction,
                FileIsEmptyAction,
                FileIsWritableAction,
            ],
        )
        file1 = tempfile.mkstemp()[1]
        self.parser.parse_args(["--file", file1])
        # Can now confidently know that
        # 1. file1 exists
        # 2. file1 is empty
        # 3. file1 is writable
        with open(file1, "w") as f:
            f.write("write with no valuerrors")
        os.remove(file1)

    def test_on_multiple_actions_with_one_failure(self):
        """
        Test for multiple actions of the same.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--file",
            nargs="+",
            action=PipelineAction,
            action_values=[
                FileExistsAction,
                FileIsEmptyAction,
                FileIsWritableAction,
            ],
        )
        file1 = tempfile.mkstemp()[1]
        self.parser.parse_args(["--file", file1])
        # Can now confidently know that
        # 1. file1 exists
        # 2. file1 is empty
        # 3. file1 is writable
        with open(file1, "w") as f:
            f.write("write with no valuerrors")

        # file1 no longer empty. Assert ValueError raised
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--file", file1])

        os.remove(file1)
        # file1 no longer exists. assert ValueError raised
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--file", file1])


class TestPipelineActionSolo(ActionHeroTestCase):
    def test_on_nonaction_hero_action_in_action_values(self):
        """
        Sets the action for action.

        Args:
            self: (todo): write your description
        """
        class UnrecognizedAction(argparse.Action):
            def __call__(self, parser, namespace, values, option_string=None):
                """
                Call the given parser with the specified parser.

                Args:
                    self: (todo): write your description
                    parser: (todo): write your description
                    namespace: (str): write your description
                    values: (array): write your description
                    option_string: (str): write your description
                """
                pass

        with self.assertRaises(ValueError):
            self.parser.add_argument(
                "--word",
                action=PipelineAction,
                action_values=[UnrecognizedAction],
            )

    @run_only_when_modules_loaded(modules=["action_hero"])
    def test_on_action_that_accepts_action_values(self):
        """
        Test if the action was executed.

        Args:
            self: (todo): write your description
        """
        # 1. Code to run argumentparser and parse args
        script_contents = """
import argparse
from action_hero.utils import PipelineAction
from action_hero import FileHasExtensionAction, FileDoesNotExistAction

# p = ExitCapturedArgumentParser()
p = argparse.ArgumentParser()
p.add_argument(
    "--readme",
    action=PipelineAction,
    nargs="+",
    action_values=[
        (FileHasExtensionAction, ["md", "markdown"]),
        FileDoesNotExistAction,
    ],
)
args = p.parse_args(["--readme", "DAILY.md", "another.markdown"])
print(args.readme)
"""
        # 2. Create a temporary file
        with tempfile.NamedTemporaryFile(suffix=".py") as script_file:
            # 3. Write into temporary sciptfile
            with open(script_file.name, "w") as f:
                f.write(script_contents)

            # 4. Run temp_script_file as a subprocess
            from subprocess import PIPE, run
            import sys

            script_result = run(
                [sys.executable, script_file.name],
                stdin=PIPE,
                stdout=PIPE,
                stderr=PIPE,
            )
            # 5. Assert subprocess stderr is empty string
            self.assertFalse(script_result.stderr)


class TestDisplayMessageAndExitAction(ActionHeroTestCase):
    def test_if_is_subclass_of_argparse_action(self):
        """
        Assign an argparse action to an argparse action.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(
            issubclass(DisplayMessageAndExitAction, argparse.Action)
        )

    def test_if_is_subclass_of_actionhero_action(self):
        """
        Assigns the actionhero action.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(
            issubclass(DisplayMessageAndExitAction, ActionHeroAction)
        )
