import os
import unittest
import tempfile
from argparse import ArgumentParser

from action_heroes.path import (
    EnsureDirectoryAction,
    EnsureFileAction,
    ResolvePathAction,
    PathIsValidAction,
)
from action_heroes.path_utils import resolve_path, is_valid_path, is_valid_file


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


class TestPathIsValidAction(ParserEnclosedTestCase):
    def test_valid_path_on_valid_path(self):
        self.parser.add_argument("--path", action=PathIsValidAction)
        with tempfile.TemporaryDirectory() as path:
            # Assert path is valid path
            self.assertTrue(is_valid_path(path))
            # Parse args with list of paths
            args = self.parser.parse_args(["--path", path])
            # Assert path from args is valid path
            self.assertTrue(is_valid_path(args.path))

    def test_valid_path_on_multiple_valid_paths(self):
        self.parser.add_argument("--path", nargs="+", action=PathIsValidAction)

        # Create few temporary paths
        path1 = tempfile.mkdtemp()
        path2 = tempfile.mkdtemp()
        path3 = tempfile.mkdtemp()
        paths = [path1, path2, path3]

        # Parse args with list of paths
        self.parser.parse_args(["--path", *paths])
        self.assertNotIn(False, [is_valid_path(p) for p in paths])

        # Delete all temporary paths
        [os.rmdir(path) for path in paths]

    def test_valid_path_on_invalid_path(self):
        self.parser.add_argument("--path", action=PathIsValidAction)
        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a file name with a char forbidden in POSIX and WIN*
            forbidden_char = "/"
            file_name = "SOMEFILE{}".format(forbidden_char)
            file_path = os.path.join(parent_directory, file_name)

            # Assert that the forbidden character prohibited path creation
            self.assertFalse(is_valid_path(file_path))

            with self.assertRaises(ValueError):
                # Parse args with prohibited filename
                self.parser.parse_args(["--path", file_path])

    def test_valid_path_on_mixed_valid_and_invalid_path(self):
        self.parser.add_argument("--path", nargs="+", action=PathIsValidAction)

        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a file name with a char forbidden in POSIX and WIN*
            forbidden_char = "/"
            invalid_path_name = "SOMEFILE{}".format(forbidden_char)
            invalid_path = os.path.join(parent_directory, invalid_path_name)

            # Assert that the forbidden character prohibited path creation
            self.assertFalse(is_valid_path(invalid_path))

            # Create valid path
            with tempfile.TemporaryDirectory() as valid_dir_path:

                # Assemble mixed valid and invalid path
                paths = [invalid_path, valid_dir_path]

                with self.assertRaises(ValueError):
                    # Parse args with list of paths
                    self.parser.parse_args(["--path", *paths])


class TestFileIsValidAction(ParserEnclosedTestCase):
    def test_valid_file_on_valid_file_path(self):
        self.parser.add_argument("--path", action=PathIsValidAction)
        with tempfile.NamedTemporaryFile() as file_path:
            # Assert file path is valid file path
            self.assertTrue(is_valid_file(file_path.name))
            # Parse args with list of paths
            args = self.parser.parse_args(["--path", file_path.name])
            # Assert path from args is valid path
            self.assertTrue(is_valid_file(args.path))

    def test_valid_file_on_multiple_valid_file_paths(self):
        self.parser.add_argument("--path", nargs="+", action=PathIsValidAction)

        # Create few temporary paths
        file_path1 = tempfile.mkstemp()[1]
        file_path2 = tempfile.mkstemp()[1]
        file_path3 = tempfile.mkstemp()[1]
        file_paths = [file_path1, file_path2, file_path3]

        # Parse args with list of paths
        self.parser.parse_args(["--path", *file_paths])
        self.assertNotIn(False, [is_valid_path(p) for p in file_paths])

        # Delete all temporary file paths
        [os.remove(path) for path in file_paths]

    def test_valid_file_on_invalid_file_path(self):
        self.parser.add_argument("--path", action=PathIsValidAction)
        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a file name with a char forbidden in POSIX and WIN*
            forbidden_char = "/"
            file_name = "SOMEFILE{}".format(forbidden_char)
            file_path = os.path.join(parent_directory, file_name)

            # Assert that the forbidden character prohibited path creation
            self.assertFalse(is_valid_file(file_path))

            with self.assertRaises(ValueError):
                # Parse args with prohibited filename
                self.parser.parse_args(["--path", file_path])

    def test_valid_file_on_mixed_valid_and_invalid_file_path(self):
        self.parser.add_argument("--path", nargs="+", action=PathIsValidAction)

        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a file name with a char forbidden in POSIX and WIN*
            forbidden_char = "/"
            invalid_file_name = "SOMEFILE{}".format(forbidden_char)
            invalid_file_path = os.path.join(
                parent_directory, invalid_file_name
            )

            # Assert that the forbidden character prohibited path creation
            self.assertFalse(is_valid_file(invalid_file_path))

            # Create valid path
            with tempfile.NamedTemporaryFile() as valid_file_path:

                # Assemble mixed valid and invalid path
                paths = [invalid_file_path, valid_file_path.name]

                with self.assertRaises(ValueError):
                    # Parse args with list of paths
                    self.parser.parse_args(["--path", *paths])
