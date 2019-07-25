import os
import unittest
import tempfile
from argparse import ArgumentParser

from action_heroes.path import ResolvePathAction
from action_heroes.path_utils import resolve_path


class ParserEnclosedTestCase(unittest.TestCase):
    def setUp(self):
        """Setup new parser"""
        self.parser = ArgumentParser()


class TestResolvePathAction(ParserEnclosedTestCase):
    def test_resolve_path_action_processes_path(self):
        self.parser.add_argument("--path", action=ResolvePathAction)
        with tempfile.TemporaryDirectory() as temp_directory:
            args = self.parser.parse_args(["--path", temp_directory])
            self.assertIn("path", args)

    def test_resolve_path_action_resolves_single_path(self):
        self.parser.add_argument("--path", action=ResolvePathAction)
        with tempfile.TemporaryDirectory() as temp_directory:
            args = self.parser.parse_args(["--path", temp_directory])
            expected = resolve_path(temp_directory)
            self.assertEqual(args.path, expected)

    def test_resolve_path_action_resolves_list_of_paths(self):
        self.parser.add_argument("--path", nargs="+", action=ResolvePathAction)

        # Create few temporary paths
        path1 = tempfile.mkdtemp()
        path2 = tempfile.mkdtemp()
        path3 = tempfile.mkdtemp()

        temp_paths = [path1, path2, path3]

        # Parse args with list of paths
        args = self.parser.parse_args(["--path", *temp_paths])
        expected = [resolve_path(path) for path in temp_paths]
        self.assertEqual(args.path, expected)

        # Delete all temporary paths
        [os.rmdir(path) for path in temp_paths]
