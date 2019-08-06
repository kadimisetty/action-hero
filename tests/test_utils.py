import argparse
import os
import tempfile
import unittest


from action_hero.utils import (
    ActionHeroAction,
    ActionHeroTestCase,
    ExitCapturedArgumentParser,
    run_only_when_modules_loaded,
    run_only_when_when_internet_is_up,
)
from action_hero.utils import (
    BaseAction,
    CheckAction,
    CheckPresentInValuesAction,
    MapAction,
    MapAndReplaceAction,
    PipelineAction,
)
from action_hero import (
    FileDoesNotExistAction,
    FileExistsAction,
    FileIsEmptyAction,
    FileIsReadableAction,
    FileIsWritableAction,
    FilenameHasExtension,
)


class TestRunOnlyWhenWhenInternetIsUp(ActionHeroTestCase):
    def test_on_reachable_url(self):
        @run_only_when_when_internet_is_up(urls="AAA")
        def func():
            raise ValueError

        # Should not run this func since the url is invalid and unreachable
        func()


class TestRunOnlyWhenModuleLoaded(unittest.TestCase):
    def test_on_available_module_unittest(self):
        @run_only_when_modules_loaded(modules=["sys"])
        def raise_value_error():
            raise ValueError()

        # Assert that func raise_value_error runs
        with self.assertRaises(ValueError):
            raise_value_error()

    def test_on_unavailable_module_unittest(self):
        @run_only_when_modules_loaded(modules=["unavailable_module_xyz"])
        def raise_value_error():
            raise ValueError()

        # func raise_value_error does not run
        raise_value_error()


class TestActionHeroTestCase(ActionHeroTestCase):
    def test_argparse_argument_parser_is_present(self):
        self.assertTrue(hasattr(self, "parser"))

    def test_argparse_argument_parser_is_instance_of_argument_parser(self):
        self.assertIsInstance(self.parser, argparse.ArgumentParser)

    def test_argparse_argument_parser_is_instance_of_custom_parser(self):
        self.assertIsInstance(self.parser, ExitCapturedArgumentParser)

    def test_is_subclassed_of_unittest_testcase(self):
        self.assertTrue(issubclass(ActionHeroTestCase, unittest.TestCase))


class TestBaseAction(ActionHeroTestCase):
    def test_if_is_subclass_of_argparse_action(self):
        self.assertTrue(issubclass(BaseAction, argparse.Action))


class TestCheckAction(ActionHeroTestCase):
    def test_if_is_subclass_of_argparse_action(self):
        self.assertTrue(issubclass(CheckAction, argparse.Action))

    def test_if_checks_for_required_func(self):
        class CheckActionWithotFunc(CheckAction):
            err_msg_singular = "S"
            err_msg_plural = "P"

        with self.assertRaises(ValueError):
            CheckActionWithotFunc(option_strings=[], dest="")

    def test_if_checks_for_required_err_msg_singular(self):
        class CheckActionWithotErrMsgSingular(CheckAction):
            func = print
            err_msg_plural = "P"

        with self.assertRaises(ValueError):
            CheckActionWithotErrMsgSingular(option_strings=[], dest="")

    def test_if_checks_for_required_err_msg_plural(self):
        class CheckActionWithotErrMsgSingular(CheckAction):
            func = print
            err_msg_singular = "S"

        with self.assertRaises(ValueError):
            CheckActionWithotErrMsgSingular(option_strings=[], dest="")


class TestMapAction(ActionHeroTestCase):
    def test_if_is_subclass_of_argparse_action(self):
        self.assertTrue(issubclass(MapAction, argparse.Action))

    def test_if_checks_for_required_func(self):
        class MapActionWithotFunc(MapAction):
            pass

        with self.assertRaises(ValueError):
            MapActionWithotFunc(option_strings=[], dest="")


class TestMapAndReplaceAction(ActionHeroTestCase):
    def test_if_is_subclass_of_argparse_action(self):
        self.assertTrue(issubclass(MapAndReplaceAction, argparse.Action))

    def test_if_checks_for_required_func(self):
        class MapAndReplaceWithotFunc(MapAndReplaceAction):
            pass

        with self.assertRaises(ValueError):
            MapAndReplaceWithotFunc(option_strings=[], dest="")


class TestCheckPresentInValuesAction(ActionHeroTestCase):
    def test_on_subclass_of_argparse_action(self):
        self.assertTrue(
            issubclass(CheckPresentInValuesAction, argparse.Action)
        )

    def test_on_action_value_that_is_not_a_list(self):
        class Action1(CheckPresentInValuesAction):
            def func(value):
                return value

            err_msg_singular = "S"
            err_msg_plural = "P"

        with self.assertRaises(ValueError):
            self.parser.add_argument(
                "--number", action=Action1, action_values=()
            )


    def test_on_empty_action_values(self):
        class Action1(CheckPresentInValuesAction):
            def func(value):
                return value

            err_msg_singular = "S"
            err_msg_plural = "P"

        with self.assertRaises(ValueError):
            self.parser.add_argument(
                "--number", action=Action1, action_values=[]
            )

    def test_on__required_func_and_err_msgs(self):
        class Action1(CheckPresentInValuesAction):
            pass

        with self.assertRaises(ValueError):
            Action1(option_strings=[], dest="", action_values=["UV"])

    def test_on_required_value(self):
        class Action1(CheckPresentInValuesAction):
            def func(value):
                return value

            err_msg_singular = "S"
            err_msg_plural = "P"

        with self.assertRaises(ValueError):
            Action1(option_strings=[], dest="")

    def test_on_action_values_with_uneven_types(self):
        class Action1(CheckPresentInValuesAction):
            def func(value):
                return value

            err_msg_singular = "S"
            err_msg_plural = "P"

        with self.assertRaises(ValueError):
            self.parser.add_argument(
                "--color", action=Action1, action_values=["red", "blue", 2]
            )

    def test_on_action_values_with_type_specified(self):
        class Action1(CheckPresentInValuesAction):
            def func(value):
                return value

            err_msg_singular = "S"
            err_msg_plural = "P"

        self.parser.add_argument(
            "--number", action=Action1, type=int, action_values=[1, 2, 3]
        )

        self.parser.parse_args(["--number", "2"])

    def test_on_action_values_with_unheeded_type_specified(self):
        class Action1(CheckPresentInValuesAction):
            def func(value):
                return value

            err_msg_singular = "S"
            err_msg_plural = "P"

        self.parser.add_argument(
            "--number", action=Action1, action_values=[4, 5, 6]
        )

        with self.assertRaises(ValueError):
            self.parser.parse_args(["--number", "5"])

    def test_on_action_values_with_mixed_type_specified(self):
        class Action1(CheckPresentInValuesAction):
            def func(value):
                return value

            err_msg_singular = "S"
            err_msg_plural = "P"

        with self.assertRaises(ValueError):
            self.parser.add_argument(
                "--number", action=Action1, action_values=[4, 5, "6"]
            )

    def test_on_uncastable_action_value_entry(self):
        class Action1(CheckPresentInValuesAction):
            def func(value):
                return value

            err_msg_singular = "S"
            err_msg_plural = "P"

        self.parser.add_argument(
            "--number",
            action=Action1,
            action_values=["four"],
            type=int,
        )

        with self.assertRaises(ValueError):
            self.parser.parse_args(["--number", "4"])


class TestActionHeroAction(ActionHeroTestCase):
    def test_if_is_subclass_of_argparse_action(self):
        self.assertTrue(issubclass(ActionHeroAction, argparse.Action))


class TestPipelineAction(ActionHeroTestCase):
    """Known issue with testing PipelineActions using actions w/ action_values
    tends to cause errors where some test cases do not have any content for
    values"""

    def test_if_is_subclass_of_actionheroaction(self):
        self.assertTrue(issubclass(PipelineAction, ActionHeroAction))

    def test_on_child_action(self):
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
        with self.assertRaises(ValueError):
            self.parser.add_argument(
                "--file", action=PipelineAction, action_values=[]
            )

    def test_on_action_value_of_wrong_type_int(self):
        with self.assertRaises(ValueError):
            self.parser.add_argument(
                "--file", action=PipelineAction, action_values=5
            )

    def test_on_action_value_of_wrong_type_str(self):
        with self.assertRaises(ValueError):
            self.parser.add_argument(
                "--file", action=PipelineAction, action_values=5
            )

    def test_on_action_value_of_wrong_type_action_with_no_list(self):
        with self.assertRaises(ValueError):
            self.parser.add_argument(
                "--file", action=PipelineAction, action_values=FileExistsAction
            )

    def test_on_list_of_child_multiple_actions(self):
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


class SoloTestCase(ActionHeroTestCase):
    def test_on_nonaction_hero_action_in_action_values(self):
        class UnrecognizedAction(argparse.Action):
            def __call__(self, parser, namespace, values, option_string=None):
                pass

        with self.assertRaises(ValueError):
            self.parser.add_argument(
                "--word",
                action=PipelineAction,
                action_values=[UnrecognizedAction],
            )

    @run_only_when_modules_loaded(modules=["action_hero"])
    def test_on_action_that_accepts_action_values(self):
        # 1. Code to run argumentparser and parse args
        script_contents = """
import argparse
from action_hero.utils import PipelineAction
from action_hero import FilenameHasExtension, FileDoesNotExistAction

# p = ExitCapturedArgumentParser()
p = argparse.ArgumentParser()
p.add_argument(
    "--readme",
    action=PipelineAction,
    nargs="+",
    action_values=[
        (FilenameHasExtension, ["md", "markdown"]),
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
