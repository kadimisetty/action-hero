import os
import unittest
import tempfile
from argparse import ArgumentParser

from action_heroes.path import (
    EnsureDirectoryAction,
    EnsureFileAction,
    ResolvePathAction,
)
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


class TestEnsureDirectoryAction(ParserEnclosedTestCase):
    def test_ensure_directory_on_nonexisting_directory(self):
        self.parser.add_argument("--path", action=EnsureDirectoryAction)
        with tempfile.TemporaryDirectory() as parent_directory:
            # Specify unique directory name
            directory_to_check = os.path.join(parent_directory, "NEWDIRT")
            # Assert specified directory does not exist
            self.assertFalse(os.path.isdir(directory_to_check))
            # Parse args with --path as specified directory
            self.parser.parse_args(["--path", directory_to_check])
            # Assert specified directory does exist
            self.assertTrue(os.path.isdir(directory_to_check))

    def test_ensure_directory_on_existing_directory(self):
        self.parser.add_argument("--path", action=EnsureDirectoryAction)
        # Specify directory to check
        with tempfile.TemporaryDirectory() as directory_to_check:
            # Assert specified directory exists
            self.assertTrue(os.path.isdir(directory_to_check))
            # Parse args with --path as specified directory
            self.parser.parse_args(["--path", directory_to_check])
            # Assert specified directory still exist
            self.assertTrue(os.path.isdir(directory_to_check))

    def test_ensure_directory_on_multiple_mixed_existing_directories(self):
        self.parser.add_argument(
            "--path", nargs="+", action=EnsureDirectoryAction
        )

        # Specify few new temporary directories
        dir1 = tempfile.mkdtemp()
        dir2 = tempfile.mkdtemp()

        # Directories deleted immediately to confirm they do not exist
        dir3 = tempfile.mkdtemp()
        os.rmdir(dir3)
        dir4 = tempfile.mkdtemp()
        os.rmdir(dir4)

        mixed_dirs = [dir1, dir2, dir3, dir4]

        # Assert that mixed_dirs contain existing and non-existing directories
        self.assertIn(True, [os.path.isdir(d) for d in mixed_dirs])
        self.assertIn(False, [os.path.isdir(d) for d in mixed_dirs])

        # Parse args with --path as specified file that does not exist
        self.parser.parse_args(["--path", *mixed_dirs])

        # Assert that all directories in mixed_dirs now exist
        self.assertNotIn(False, [os.path.isdir(d) for d in mixed_dirs])

        # Tear down temporary directories
        [os.rmdir(d) for d in mixed_dirs]


class TestEnsureFileAction(ParserEnclosedTestCase):
    def test_ensure_file_on_nonexisting_file(self):
        self.parser.add_argument("--path", action=EnsureFileAction)
        with tempfile.TemporaryDirectory() as directory_to_check:
            # Specify a file to check
            file_to_check = tempfile.mkstemp(dir=directory_to_check)[1]
            # Assert specified  file exists
            self.assertTrue(os.path.isfile(file_to_check))
            # Remove file
            os.remove(file_to_check)
            # Assert specified file no longer exists
            self.assertFalse(os.path.isfile(file_to_check))

            # Parse args with --path as specified file that does not exist
            self.parser.parse_args(["--path", file_to_check])
            # Assert specified file now exists
            self.assertTrue(os.path.isfile(file_to_check))

    def test_ensure_file_on_existing_file(self):
        self.parser.add_argument("--path", action=EnsureFileAction)
        # Specify file to check
        with tempfile.NamedTemporaryFile() as file_to_check:
            # Assert specified file exists
            self.assertTrue(os.path.isfile(file_to_check.name))
            # Parse args with --path as specified file
            self.parser.parse_args(["--path", file_to_check.name])
            # Assert specified file still exists
            self.assertTrue(os.path.isfile(file_to_check.name))

    def test_ensure_file_on_multiple_mixed_existing_files(self):
        self.parser.add_argument("--path", nargs="+", action=EnsureFileAction)
        with tempfile.TemporaryDirectory() as parent_directory:
            # Specify few new temporary files
            file1 = tempfile.mkstemp(dir=parent_directory)[1]
            file2 = tempfile.mkstemp(dir=parent_directory)[1]

            # files deleted immediately to confirm they do not exist
            file3 = tempfile.mkstemp(dir=parent_directory)[1]
            os.remove(file3)
            file4 = tempfile.mkstemp(dir=parent_directory)[1]
            os.remove(file4)

            mixed_files = [file1, file2, file3, file4]

            # Assert that mixed_files contain existing and non-existing files
            self.assertIn(True, [os.path.isfile(f) for f in mixed_files])
            self.assertIn(False, [os.path.isfile(f) for f in mixed_files])

            # Parse args with --path as specified file that does not exist
            self.parser.parse_args(["--path", *mixed_files])

            # Assert that all files in mixed_files now exist
            self.assertNotIn(False, [os.path.isfile(f) for f in mixed_files])

            # Tear down temporary files
            [os.remove(f) for f in mixed_files]
