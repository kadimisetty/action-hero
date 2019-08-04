import unittest
import argparse


from action_heroes.utils import (
    ActionHeroesTestCase,
    ExitCapturedArgumentParser,
)
from action_heroes.utils import (
    BaseAction,
    CheckAction,
    CheckPresentInValuesAction,
    MapAction,
    MapAndReplaceAction,
)


@unittest.skip("TODO")
class TestRunOnlyWhenWhenInternetIsUp(ActionHeroesTestCase):
    pass


class TestActionHeroesTestCase(ActionHeroesTestCase):
    def test_argparse_argument_parser_is_present(self):
        self.assertTrue(hasattr(self, "parser"))

    def test_argparse_argument_parser_is_instance_of_argument_parser(self):
        self.assertIsInstance(self.parser, argparse.ArgumentParser)

    def test_argparse_argument_parser_is_instance_of_custom_parser(self):
        self.assertIsInstance(self.parser, ExitCapturedArgumentParser)

    def test_is_subclassed_of_unittest_testcase(self):
        import unittest

        self.assertTrue(issubclass(ActionHeroesTestCase, unittest.TestCase))


class TestBaseAction(ActionHeroesTestCase):
    def test_if_is_subclass_of_argparse_action(self):
        self.assertTrue(issubclass(BaseAction, argparse.Action))


class TestCheckAction(ActionHeroesTestCase):
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


class TestMapAction(ActionHeroesTestCase):
    def test_if_is_subclass_of_argparse_action(self):
        self.assertTrue(issubclass(MapAction, argparse.Action))

    def test_if_checks_for_required_func(self):
        class MapActionWithotFunc(MapAction):
            pass

        with self.assertRaises(ValueError):
            MapActionWithotFunc(option_strings=[], dest="")


class TestMapAndReplaceAction(ActionHeroesTestCase):
    def test_if_is_subclass_of_argparse_action(self):
        self.assertTrue(issubclass(MapAndReplaceAction, argparse.Action))

    def test_if_checks_for_required_func(self):
        class MapAndReplaceWithotFunc(MapAndReplaceAction):
            pass

        with self.assertRaises(ValueError):
            MapAndReplaceWithotFunc(option_strings=[], dest="")


class TestCheckPresentInValuesAction(ActionHeroesTestCase):
    def test_if_is_subclass_of_argparse_action(self):
        self.assertTrue(
            issubclass(CheckPresentInValuesAction, argparse.Action)
        )

    def test_if_checks_for_required_func_and_err_msgs(self):
        class CheckPresentInValuesActionSubClassWithoutFuncAndErrMsgs(
            CheckPresentInValuesAction
        ):
            pass

        with self.assertRaises(ValueError):
            CheckPresentInValuesActionSubClassWithoutFuncAndErrMsgs(
                option_strings=[], dest="", action_values=["UV"]
            )

    def test_if_checks_for_required_value(self):
        class CheckPresentInValuesActionSubClassWithoutValue(
            CheckPresentInValuesAction
        ):
            func = print
            err_msg_singular = "S"
            err_msg_plural = "P"

        with self.assertRaises(ValueError):
            CheckPresentInValuesActionSubClassWithoutValue(
                option_strings=[], dest=""
            )
