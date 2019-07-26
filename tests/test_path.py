import os
import unittest
import tempfile
from argparse import ArgumentParser

from action_heroes.path import (
    DirectoryDoesNotExistAction,
    DirectoryExistsAction,
    DirectoryIsValidAction,
    EnsureDirectoryAction,
    EnsureFileAction,
    FileDoesNotExistAction,
    FileExistsAction,
    PathDoesNotExistsAction,
    PathExistsAction,
    PathIsValidAction,
    ResolvePathAction,
)
from action_heroes.path_utils import (
    is_existing_file,
    is_existing_path,
    is_existing_directory,
    is_executable_file,
    is_valid_directory,
    is_valid_file,
    is_valid_path,
    resolve_path,
)


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


class TestDirectoryIsValidAction(ParserEnclosedTestCase):
    def test_valid_directory_on_valid_directory_path(self):
        self.parser.add_argument("--path", action=DirectoryIsValidAction)
        with tempfile.TemporaryDirectory() as path:
            # Assert path is valid path
            self.assertTrue(is_valid_directory(path))
            # Parse args with list of paths
            args = self.parser.parse_args(["--path", path])
            # Assert path from args is valid path
            self.assertTrue(is_valid_directory(args.path))

    def test_valid_directory_on_multiple_valid_directory_paths(self):
        self.parser.add_argument(
            "--path", nargs="+", action=DirectoryIsValidAction
        )

        # Create few temporary paths
        path1 = tempfile.mkdtemp()
        path2 = tempfile.mkdtemp()
        path3 = tempfile.mkdtemp()
        paths = [path1, path2, path3]

        # Parse args with list of paths
        self.parser.parse_args(["--path", *paths])
        self.assertNotIn(False, [is_valid_directory(p) for p in paths])

        # Delete all temporary file paths
        [os.rmdir(path) for path in paths]

    def test_valid_directory_on_invalid_directory_path(self):
        self.parser.add_argument("--path", action=PathIsValidAction)
        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a file name with a char forbidden in POSIX and WIN*
            forbidden_char = "/"
            dir_name = "SOMEFILE{}".format(forbidden_char)
            dir_path = os.path.join(parent_directory, dir_name)

            # Assert that the forbidden character prohibited path creation
            self.assertFalse(is_valid_file(dir_path))

            with self.assertRaises(ValueError):
                # Parse args with prohibited filename
                self.parser.parse_args(["--path", dir_path])

    def test_valid_file_on_mixed_valid_and_invalid_file_path(self):
        self.parser.add_argument("--path", nargs="+", action=PathIsValidAction)

        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a file name with a char forbidden in POSIX and WIN*
            forbidden_char = "/"
            invalid_dir_name = "SOMEDIR{}".format(forbidden_char)
            invalid_dir_path = os.path.join(parent_directory, invalid_dir_name)

            # Assert that the forbidden character prohibited path creation
            self.assertFalse(is_valid_file(invalid_dir_path))

            # Create valid path
            with tempfile.TemporaryDirectory() as valid_dir_path:

                # Assemble mixed valid and invalid path
                paths = [invalid_dir_path, valid_dir_path]

                with self.assertRaises(ValueError):
                    # Parse args with list of paths
                    self.parser.parse_args(["--path", *paths])


class TestPathExistsAction(ParserEnclosedTestCase):
    def test_path_exists_on_existing_path(self):
        self.parser.add_argument("--path", action=PathExistsAction)
        # Specify file to check
        with tempfile.NamedTemporaryFile() as file_to_check:
            # Assert specified file exists
            self.assertTrue(is_existing_path(file_to_check.name))
            # Parse args with --path as specified file
            self.parser.parse_args(["--path", file_to_check.name])
            # Assert specified file still exists
            self.assertTrue(is_existing_path(file_to_check.name))

    def test_path_exists_on_nonexisting_path(self):
        self.parser.add_argument("--path", action=PathExistsAction)
        with tempfile.TemporaryDirectory() as directory_to_check:
            # Specify a file to check
            file_to_check = tempfile.mkstemp(dir=directory_to_check)[1]
            # Assert specified  file exists
            self.assertTrue(is_existing_path(file_to_check))
            # Remove file
            os.remove(file_to_check)
            # Assert specified file no longer exists
            self.assertFalse(is_existing_path(file_to_check))

            with self.assertRaises(ValueError):
                # Parse args with --path as specified file that does not exist
                self.parser.parse_args(["--path", file_to_check])

    def test_path_exists_on_mixed_existing_and_nonexisting_path(self):
        self.parser.add_argument("--path", nargs="+", action=PathExistsAction)
        with tempfile.TemporaryDirectory() as directory_to_check:
            # Specify a file to check
            file_to_check = tempfile.mkstemp(dir=directory_to_check)[1]
            # Assert specified  file exists
            self.assertTrue(is_existing_path(file_to_check))
            # Remove file
            os.remove(file_to_check)
            # Assert specified file no longer exists
            self.assertFalse(is_existing_path(file_to_check))
            # Assemble mixed list of existing and nonexisting paths
            paths = [directory_to_check, file_to_check]

            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", *paths])


class TestPathDoesNotExistsAction(ParserEnclosedTestCase):
    def test_path_does_not_exist_on_existing_path(self):
        self.parser.add_argument("--path", action=PathDoesNotExistsAction)
        # Specify file to check
        with tempfile.NamedTemporaryFile() as file_to_check:
            with self.assertRaises(ValueError):
                # Parse args with --path as specified file that does not exist
                self.parser.parse_args(["--path", file_to_check.name])

    def test_path_does_not_exists_on_nonexisting_path(self):
        self.parser.add_argument("--path", action=PathDoesNotExistsAction)
        with tempfile.TemporaryDirectory() as directory_to_check:
            # Specify a file to check
            file_to_check = tempfile.mkstemp(dir=directory_to_check)[1]
            # Assert specified  file exists
            self.assertTrue(is_existing_path(file_to_check))
            # Remove file
            os.remove(file_to_check)
            # Assert specified file no longer exists
            self.assertFalse(is_existing_path(file_to_check))
            # Parse args with --path as specified file
            self.parser.parse_args(["--path", file_to_check])
            # Assert specified file no longer exists
            self.assertFalse(is_existing_path(file_to_check))

    def test_path_does_not_exist_on_mixed_existing_and_nonexisting_path(self):
        self.parser.add_argument(
            "--path", nargs="+", action=PathDoesNotExistsAction
        )
        with tempfile.TemporaryDirectory() as directory_to_check:
            # Specify a file to check
            file_to_check = tempfile.mkstemp(dir=directory_to_check)[1]
            # Assert specified  file exists
            self.assertTrue(is_existing_path(file_to_check))
            # Remove file
            os.remove(file_to_check)
            # Assert specified file no longer exists
            self.assertFalse(is_existing_path(file_to_check))
            # Assemble mixed list of existing and nonexisting paths
            paths = [directory_to_check, file_to_check]

            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", *paths])


class TestFileExistsAction(ParserEnclosedTestCase):
    def test_file_exists_on_existing_path(self):
        self.parser.add_argument("--path", action=FileExistsAction)
        # Specify file to check
        with tempfile.NamedTemporaryFile() as file_to_check:
            # Assert specified file exists
            self.assertTrue(is_existing_file(file_to_check.name))
            # Parse args with --path as specified file
            self.parser.parse_args(["--path", file_to_check.name])
            # Assert specified file still exists
            self.assertTrue(is_existing_file(file_to_check.name))

    def test_file_exists_on_nonexisting_file(self):
        self.parser.add_argument("--path", action=FileExistsAction)
        with tempfile.TemporaryDirectory() as directory_to_check:
            # Specify a file to check
            file_to_check = tempfile.mkstemp(dir=directory_to_check)[1]
            # Assert specified  file exists
            self.assertTrue(is_existing_file(file_to_check))
            # Remove file
            os.remove(file_to_check)
            # Assert specified file no longer exists
            self.assertFalse(is_existing_file(file_to_check))

            with self.assertRaises(ValueError):
                # Parse args with --path as specified file that does not exist
                self.parser.parse_args(["--path", file_to_check])

    def test_file_exists_on_mixed_existing_and_nonexisting_path(self):
        self.parser.add_argument("--path", nargs="+", action=FileExistsAction)
        with tempfile.TemporaryDirectory() as directory:
            # Specify file to check
            file1 = tempfile.mkstemp(dir=directory)[1]
            file2 = tempfile.mkstemp(dir=directory)[1]
            file3 = tempfile.mkstemp(dir=directory)[1]
            # Assert specified files exists
            self.assertTrue(is_existing_file(file1))
            self.assertTrue(is_existing_file(file2))
            self.assertTrue(is_existing_file(file3))
            # Remove file 1
            os.remove(file1)
            # Assert specified file no longer exists
            self.assertFalse(is_existing_file(file1))
            # Assemble mixed list of existing and nonexisting paths
            paths = [file1, file2, file3]

            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", *paths])


class TestFileDoesNotExistsAction(ParserEnclosedTestCase):
    def test_file_does_not_exist_on_existing_path(self):
        self.parser.add_argument("--path", action=FileDoesNotExistAction)
        # Specify file to check
        with tempfile.NamedTemporaryFile() as file1:
            with self.assertRaises(ValueError):
                # Parse args with --path as specified file that does not exist
                self.parser.parse_args(["--path", file1.name])

    def test_file_does_not_exists_on_nonexisting_path(self):
        self.parser.add_argument("--path", action=FileDoesNotExistAction)
        with tempfile.TemporaryDirectory() as directory:
            # Specify a file to check
            file1 = tempfile.mkstemp(dir=directory)[1]
            # Assert specified  file exists
            self.assertTrue(is_existing_file(file1))
            # Remove file
            os.remove(file1)
            # Assert specified file no longer exists
            self.assertFalse(is_existing_file(file1))
            # Parse args with --path as specified file
            self.parser.parse_args(["--path", file1])
            # Assert specified file no longer exists
            self.assertFalse(is_existing_file(file1))

    def test_file_does_not_exist_on_mixed_existing_and_nonexisting_path(self):
        self.parser.add_argument(
            "--path", nargs="+", action=FileDoesNotExistAction
        )
        # Specify a file to check
        file1 = tempfile.mkstemp()[1]
        file2 = tempfile.mkstemp()[1]
        # Assert specified file exists
        self.assertTrue(is_existing_file(file1))
        self.assertTrue(is_existing_file(file2))
        # Remove file
        os.remove(file1)
        self.assertFalse(is_existing_file(file1))
        # Assemble mixed list of existing and nonexisting paths
        paths = [file1, file2]

        with self.assertRaises(ValueError):
            self.parser.parse_args(["--path", *paths])

        # Tear down remaining temporary files
        os.remove(file2)


class TestDirectoryExistsAction(ParserEnclosedTestCase):
    def test_directory_exists_on_existing_path(self):
        self.parser.add_argument("--path", action=DirectoryExistsAction)
        # Specify directory to check
        with tempfile.TemporaryDirectory() as directory:
            # Assert specified directory exists
            self.assertTrue(is_existing_directory(directory))
            # Parse args with --path as specified directory
            self.parser.parse_args(["--path", directory])
            # Assert specified directory still exists
            self.assertTrue(is_existing_path(directory))

    def test_directory_exists_on_nonexisting_path(self):
        self.parser.add_argument("--path", action=DirectoryExistsAction)
        # Specifiy directory
        directory1 = tempfile.mkdtemp()
        # Assert specified directory exists
        self.assertTrue(is_existing_directory(directory1))
        # Remove specified directory
        os.rmdir(directory1)
        # Assert specified directory doesnt exist
        self.assertFalse(is_existing_directory(directory1))

        with self.assertRaises(ValueError):
            # Parse args with list of paths
            self.parser.parse_args(["--path", directory1])

    def test_path_exists_on_mixed_existing_and_nonexisting_path(self):
        self.parser.add_argument("--path", action=DirectoryExistsAction)
        # Specifiy directores
        directory1 = tempfile.mkdtemp()
        directory2 = tempfile.mkdtemp()
        # Assert specified directory exists
        self.assertTrue(is_existing_directory(directory1))
        self.assertTrue(is_existing_directory(directory2))
        # Remove specified directory
        os.rmdir(directory1)
        # Assert specified directory doesnt exist
        self.assertFalse(is_existing_directory(directory1))

        with self.assertRaises(ValueError):
            # Parse args with list of paths
            self.parser.parse_args(["--path", directory1, directory2])


class TestDirectoryDoesNotExistsAction(ParserEnclosedTestCase):
    def test_directory_does_not_exist_on_existing_path(self):
        self.parser.add_argument("--path", action=DirectoryDoesNotExistAction)
        with tempfile.TemporaryDirectory() as directory1:
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", directory1])

    def test_directory_does_not_exists_on_nonexisting_path(self):
        self.parser.add_argument("--path", action=DirectoryDoesNotExistAction)
        # Specify directory
        directory1 = tempfile.mkdtemp()
        # Assert directory exists
        self.assertTrue(is_existing_directory(directory1))
        # Remove specified directory
        os.rmdir(directory1)
        # Pargs args with removed specified directory
        self.parser.parse_args(["--path", directory1])

    def test_path_does_not_exist_on_mixed_existing_and_nonexisting_path(self):
        self.parser.add_argument(
            "--path", nargs="+", action=DirectoryDoesNotExistAction
        )
        # Specify directories
        directory1 = tempfile.mkdtemp()
        directory2 = tempfile.mkdtemp()
        # Assert directories exists
        self.assertTrue(is_existing_directory(directory1))
        self.assertTrue(is_existing_directory(directory2))
        # Remove one specified directory
        os.rmdir(directory1)
        # Pargs args with one removed specified directory
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--path", directory1, directory2])
        # Tear down remaining temporary directories
        os.rmdir(directory2)
