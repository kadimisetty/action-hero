import unittest
import argparse


from action_heroes.utils import (
    ActionHeroesTestCase,
    ExitCapturedArgumentParser,
)
from action_heroes.utils import (
    BaseAction,
    CheckAction,
    MapAction,
    MapAndReplaceAction,
)


@unittest.skip("TODO")
class TestRunOnlyWhenWhenInternetIsUp(ActionHeroesTestCase):
    pass


class TestActionHeroesTestCase(ActionHeroesTestCase):
    def test_argparse_argument_parser_is_present(self):
        self.assertTrue(hasattr(self, "parser"))

    def test_argparse_argument_parser_is_subclass_of_argument_parser(self):
        self.assertIsInstance(self.parser, argparse.ArgumentParser)

    def test_argparse_argument_parser_is_subclass_of_custom_parser(self):
        self.assertIsInstance(self.parser, ExitCapturedArgumentParser)

    def test_is_subclassed_of_unittest_testcase(self):
        import unittest

        self.assertTrue(issubclass(ActionHeroesTestCase, unittest.TestCase))


@unittest.skip("TODO")
class TestBaseAction(ActionHeroesTestCase):
    pass


@unittest.skip("TODO")
class TestCheckAction(ActionHeroesTestCase):
    pass


@unittest.skip("TODO")
class TestMapAction(ActionHeroesTestCase):
    pass


@unittest.skip("TODO")
class TestMapAndReplaceAction(ActionHeroesTestCase):
    pass
