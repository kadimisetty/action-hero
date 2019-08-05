import os
import tempfile

from action_hero.utils import ActionHeroTestCase
from action_hero.path import (
    DirectoryDoesNotExistAction,
    DirectoryExistsAction,
    DirectoryIsExecutableAction,
    DirectoryIsNotExecutableAction,
    DirectoryIsNotReadableAction,
    DirectoryIsNotWritableAction,
    DirectoryIsReadableAction,
    DirectoryIsValidAction,
    DirectoryIsWritableAction,
    EnsureDirectoryAction,
    EnsureFileAction,
    FileDoesNotExistAction,
    FileExistsAction,
    FileIsEmptyAction,
    FileIsExecutableAction,
    FileIsNotEmptyAction,
    FileIsNotExecutableAction,
    FileIsNotReadableAction,
    FileIsNotWritableAction,
    FileIsReadableAction,
    FileIsWritableAction,
    FilenameHasExtension,
    PathDoesNotExistsAction,
    PathExistsAction,
    PathIsExecutableAction,
    PathIsNotExecutableAction,
    PathIsNotReadableAction,
    PathIsNotWritableAction,
    PathIsReadableAction,
    PathIsValidAction,
    PathIsWritableAction,
    ResolvePathAction,
)
from action_hero.path_utils import (
    add_execute_permission,
    is_empty_file,
    is_executable_directory,
    is_executable_file,
    is_existing_directory,
    is_existing_file,
    is_existing_path,
    is_readable_directory,
    is_readable_file,
    is_readable_path,
    is_valid_directory,
    is_valid_file,
    is_valid_path,
    is_writable_file,
    remove_execute_permission,
    remove_read_permission,
    remove_write_permission,
    resolve_path,
)


class TestResolvePathAction(ActionHeroTestCase):
    def test_processes_path(self):
        self.parser.add_argument("--path", action=ResolvePathAction)
        with tempfile.TemporaryDirectory() as dir1:
            args = self.parser.parse_args(["--path", dir1])
            self.assertIn("path", args)

    def test_on_single_path(self):
        self.parser.add_argument("--path", action=ResolvePathAction)
        with tempfile.TemporaryDirectory() as dir1:
            args = self.parser.parse_args(["--path", dir1])
            expected = resolve_path(dir1)
            self.assertEqual(args.path, expected)

    def test_on_list_of_paths(self):
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


class TestEnsureDirectoryAction(ActionHeroTestCase):
    def test_on_nonexisting_directory(self):
        self.parser.add_argument("--path", action=EnsureDirectoryAction)
        with tempfile.TemporaryDirectory() as parent_directory:
            # Specify unique directory name
            dir1 = os.path.join(parent_directory, "NEWDIRT")
            # Assert specified directory does not exist
            self.assertFalse(os.path.isdir(dir1))
            # Parse args with --path as specified directory
            self.parser.parse_args(["--path", dir1])
            # Assert specified directory does exist
            self.assertTrue(os.path.isdir(dir1))

    def test_on_existing_directory(self):
        self.parser.add_argument("--path", action=EnsureDirectoryAction)
        # Specify directory to check
        with tempfile.TemporaryDirectory() as dir1:
            # Assert specified directory exists
            self.assertTrue(os.path.isdir(dir1))
            # Parse args with --path as specified directory
            self.parser.parse_args(["--path", dir1])
            # Assert specified directory still exist
            self.assertTrue(os.path.isdir(dir1))

    def test_on_multiple_mixed_existing_directories(self):
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


class TestEnsureFileAction(ActionHeroTestCase):
    def test_on_nonexisting_file(self):
        self.parser.add_argument("--path", action=EnsureFileAction)
        with tempfile.TemporaryDirectory() as dir1:
            # Specify a file to check
            file1 = tempfile.mkstemp(dir=dir1)[1]
            # Assert specified  file exists
            self.assertTrue(os.path.isfile(file1))
            # Remove file
            os.remove(file1)
            # Assert specified file no longer exists
            self.assertFalse(os.path.isfile(file1))

            # Parse args with --path as specified file that does not exist
            self.parser.parse_args(["--path", file1])
            # Assert specified file now exists
            self.assertTrue(os.path.isfile(file1))

    def test_on_existing_file(self):
        self.parser.add_argument("--path", action=EnsureFileAction)
        # Specify file to check
        with tempfile.NamedTemporaryFile() as file1:
            # Assert specified file exists
            self.assertTrue(os.path.isfile(file1.name))
            # Parse args with --path as specified file
            self.parser.parse_args(["--path", file1.name])
            # Assert specified file still exists
            self.assertTrue(os.path.isfile(file1.name))

    def test_on_multiple_mixed_existing_files(self):
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


class TestPathIsValidAction(ActionHeroTestCase):
    def test_on_valid_path(self):
        self.parser.add_argument("--path", action=PathIsValidAction)
        with tempfile.TemporaryDirectory() as path1:
            # Assert path is valid path
            self.assertTrue(is_valid_path(path1))
            # Parse args with list of paths
            args = self.parser.parse_args(["--path", path1])
            # Assert path from args is valid path
            self.assertTrue(is_valid_path(args.path))

    def test_on_multiple_valid_paths(self):
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

    def test_on_invalid_path(self):
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

    def test_on_mixed_valid_and_invalid_path(self):
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


class TestFileIsValidAction(ActionHeroTestCase):
    def test_on_valid_file_path(self):
        self.parser.add_argument("--path", action=PathIsValidAction)
        with tempfile.NamedTemporaryFile() as file_path:
            # Assert file path is valid file path
            self.assertTrue(is_valid_file(file_path.name))
            # Parse args with list of paths
            args = self.parser.parse_args(["--path", file_path.name])
            # Assert path from args is valid path
            self.assertTrue(is_valid_file(args.path))

    def test_on_multiple_valid_file_paths(self):
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

    def test_on_invalid_file_path(self):
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

    def test_on_mixed_valid_and_invalid_file_path(self):
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


class TestDirectoryIsValidAction(ActionHeroTestCase):
    def test_on_valid_directory_path(self):
        self.parser.add_argument("--path", action=DirectoryIsValidAction)
        with tempfile.TemporaryDirectory() as dir1:
            # Assert path is valid path
            self.assertTrue(is_valid_directory(dir1))
            # Parse args with list of paths
            args = self.parser.parse_args(["--path", dir1])
            # Assert path from args is valid path
            self.assertTrue(is_valid_directory(args.path))

    def test_on_multiple_valid_directory_paths(self):
        self.parser.add_argument(
            "--path", nargs="+", action=DirectoryIsValidAction
        )

        # Create few temporary paths
        dir1 = tempfile.mkdtemp()
        dir2 = tempfile.mkdtemp()
        dir3 = tempfile.mkdtemp()
        dirs = [dir1, dir2, dir3]

        # Parse args with list of paths
        self.parser.parse_args(["--path", *dirs])
        self.assertNotIn(False, [is_valid_directory(d) for d in dirs])

        # Delete all temporary file paths
        [os.rmdir(d) for d in dirs]

    def test_on_invalid_directory_path(self):
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

    def test_on_mixed_valid_and_invalid_file_path(self):
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


class TestPathExistsAction(ActionHeroTestCase):
    def test_on_existing_path(self):
        self.parser.add_argument("--path", action=PathExistsAction)
        # Specify file to check
        with tempfile.NamedTemporaryFile() as file1:
            # Assert specified file exists
            self.assertTrue(is_existing_path(file1.name))
            # Parse args with --path as specified file
            self.parser.parse_args(["--path", file1.name])
            # Assert specified file still exists
            self.assertTrue(is_existing_path(file1.name))

    def test_on_nonexisting_path(self):
        self.parser.add_argument("--path", action=PathExistsAction)
        with tempfile.TemporaryDirectory() as dir1:
            # Specify a file to check
            file1 = tempfile.mkstemp(dir=dir1)[1]
            # Assert specified  file exists
            self.assertTrue(is_existing_path(file1))
            # Remove file
            os.remove(file1)
            # Assert specified file no longer exists
            self.assertFalse(is_existing_path(file1))

            with self.assertRaises(ValueError):
                # Parse args with --path as specified file that does not exist
                self.parser.parse_args(["--path", file1])

    def test_on_mixed_existing_and_nonexisting_path(self):
        self.parser.add_argument("--path", nargs="+", action=PathExistsAction)
        with tempfile.TemporaryDirectory() as dir1:
            # Specify a file to check
            file1 = tempfile.mkstemp(dir=dir1)[1]
            # Assert specified  file exists
            self.assertTrue(is_existing_path(file1))
            # Remove file
            os.remove(file1)
            # Assert specified file no longer exists
            self.assertFalse(is_existing_path(file1))
            # Assemble mixed list of existing and nonexisting paths
            paths = [dir1, file1]

            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", *paths])


class TestPathDoesNotExistsAction(ActionHeroTestCase):
    def test_on_existing_path(self):
        self.parser.add_argument("--path", action=PathDoesNotExistsAction)
        # Specify file to check
        with tempfile.NamedTemporaryFile() as file1:
            with self.assertRaises(ValueError):
                # Parse args with --path as specified file that does not exist
                self.parser.parse_args(["--path", file1.name])

    def test_on_nonexisting_path(self):
        self.parser.add_argument("--path", action=PathDoesNotExistsAction)
        with tempfile.TemporaryDirectory() as dir1:
            # Specify a file to check
            file1 = tempfile.mkstemp(dir=dir1)[1]
            # Assert specified  file exists
            self.assertTrue(is_existing_path(file1))
            # Remove file
            os.remove(file1)
            # Assert specified file no longer exists
            self.assertFalse(is_existing_path(file1))
            # Parse args with --path as specified file
            self.parser.parse_args(["--path", file1])
            # Assert specified file no longer exists
            self.assertFalse(is_existing_path(file1))

    def test_on_mixed_existing_and_nonexisting_path(self):
        self.parser.add_argument(
            "--path", nargs="+", action=PathDoesNotExistsAction
        )
        with tempfile.TemporaryDirectory() as dir1:
            # Specify a file to check
            file1 = tempfile.mkstemp(dir=dir1)[1]
            # Assert specified  file exists
            self.assertTrue(is_existing_path(file1))
            # Remove file
            os.remove(file1)
            # Assert specified file no longer exists
            self.assertFalse(is_existing_path(file1))
            # Assemble mixed list of existing and nonexisting paths
            paths = [dir1, file1]

            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", *paths])


class TestFileExistsAction(ActionHeroTestCase):
    def test_on_existing_path(self):
        self.parser.add_argument("--path", action=FileExistsAction)
        # Specify file to check
        with tempfile.NamedTemporaryFile() as file1:
            # Assert specified file exists
            self.assertTrue(is_existing_file(file1.name))
            # Parse args with --path as specified file
            self.parser.parse_args(["--path", file1.name])
            # Assert specified file still exists
            self.assertTrue(is_existing_file(file1.name))

    def test_on_nonexisting_file(self):
        self.parser.add_argument("--path", action=FileExistsAction)
        with tempfile.TemporaryDirectory() as dir1:
            # Specify a file to check
            file1 = tempfile.mkstemp(dir=dir1)[1]
            # Assert specified  file exists
            self.assertTrue(is_existing_file(file1))
            # Remove file
            os.remove(file1)
            # Assert specified file no longer exists
            self.assertFalse(is_existing_file(file1))

            with self.assertRaises(ValueError):
                # Parse args with --path as specified file that does not exist
                self.parser.parse_args(["--path", file1])

    def test_on_mixed_existing_and_nonexisting_path(self):
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


class TestFileDoesNotExistsAction(ActionHeroTestCase):
    def test_on_existing_path(self):
        self.parser.add_argument("--path", action=FileDoesNotExistAction)
        # Specify file to check
        with tempfile.NamedTemporaryFile() as file1:
            with self.assertRaises(ValueError):
                # Parse args with --path as specified file that does not exist
                self.parser.parse_args(["--path", file1.name])

    def test_on_nonexisting_path(self):
        self.parser.add_argument("--path", action=FileDoesNotExistAction)
        with tempfile.TemporaryDirectory() as dir1:
            # Specify a file to check
            file1 = tempfile.mkstemp(dir=dir1)[1]
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

    def test_on_mixed_existing_and_nonexisting_path(self):
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


class TestDirectoryExistsAction(ActionHeroTestCase):
    def test_on_existing_path(self):
        self.parser.add_argument("--path", action=DirectoryExistsAction)
        # Specify directory to check
        with tempfile.TemporaryDirectory() as dir1:
            # Assert specified directory exists
            self.assertTrue(is_existing_directory(dir1))
            # Parse args with --path as specified directory
            args = self.parser.parse_args(["--path", dir1])
            # Assert specified directory still exists
            self.assertTrue(is_existing_path(dir1))
            self.assertTrue(is_existing_path(args.path))

    def test_on_nonexisting_path(self):
        self.parser.add_argument("--path", action=DirectoryExistsAction)
        # Specifiy directory
        dir1 = tempfile.mkdtemp()
        # Assert specified directory exists
        self.assertTrue(is_existing_directory(dir1))
        # Remove specified directory
        os.rmdir(dir1)
        # Assert specified directory doesnt exist
        self.assertFalse(is_existing_directory(dir1))

        with self.assertRaises(ValueError):
            # Parse args with list of paths
            self.parser.parse_args(["--path", dir1])

    def test_on_mixed_existing_and_nonexisting_path(self):
        self.parser.add_argument("--path", action=DirectoryExistsAction)
        # Specifiy directores
        dir1 = tempfile.mkdtemp()
        dir2 = tempfile.mkdtemp()
        # Assert specified directory exists
        self.assertTrue(is_existing_directory(dir1))
        self.assertTrue(is_existing_directory(dir2))
        # Remove specified directory
        os.rmdir(dir1)
        # Assert specified directory doesnt exist
        self.assertFalse(is_existing_directory(dir1))

        with self.assertRaises(ValueError):
            # Parse args with list of paths
            self.parser.parse_args(["--path", dir1, dir2])


class TestDirectoryDoesNotExistsAction(ActionHeroTestCase):
    def test_on_existing_path(self):
        self.parser.add_argument("--path", action=DirectoryDoesNotExistAction)
        with tempfile.TemporaryDirectory() as dir1:
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", dir1])

    def test_on_nonexisting_path(self):
        self.parser.add_argument("--path", action=DirectoryDoesNotExistAction)
        # Specify directory
        dir1 = tempfile.mkdtemp()
        # Assert directory exists
        self.assertTrue(is_existing_directory(dir1))
        # Remove specified directory
        os.rmdir(dir1)
        # Pargs args with removed specified directory
        self.parser.parse_args(["--path", dir1])

    def test_on_mixed_existing_and_nonexisting_path(self):
        self.parser.add_argument(
            "--path", nargs="+", action=DirectoryDoesNotExistAction
        )
        # Specify directories
        dir1 = tempfile.mkdtemp()
        dir2 = tempfile.mkdtemp()
        # Assert directories exists
        self.assertTrue(is_existing_directory(dir1))
        self.assertTrue(is_existing_directory(dir2))
        # Remove one specified directory
        os.rmdir(dir1)
        # Pargs args with one removed specified directory
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--path", dir1, dir2])
        # Tear down remaining temporary directories
        os.rmdir(dir2)


class TestFileIsWritableAction(ActionHeroTestCase):
    def test_on_writable_file(self):
        self.parser.add_argument("--path", action=FileIsWritableAction)
        # Specify file
        with tempfile.NamedTemporaryFile() as file1:
            # Assert fil eis writable
            self.assertTrue(is_writable_file(file1.name))
            # No errors when parsing args
            self.parser.parse_args(["--path", file1.name])
            # Assert file is still writable
            self.assertTrue(is_writable_file(file1.name))

    def test_on_unwritable_file(self):
        self.parser.add_argument("--path", action=FileIsWritableAction)
        # Specify file
        with tempfile.NamedTemporaryFile() as file1:
            # Assert fileis writable
            self.assertTrue(is_writable_file(file1.name))
            # No errors when parsing args
            self.parser.parse_args(["--path", file1.name])

    def test_on_mixed_writable_and_unwritable_file(self):
        self.parser.add_argument(
            "--path", nargs="+", action=FileIsWritableAction
        )
        with tempfile.TemporaryDirectory() as dir1:
            # Specify writable and unwritable file
            file1 = tempfile.mkstemp(dir=dir1)[1]
            file2 = tempfile.mkstemp(dir=dir1)[1]
            remove_write_permission(file2)
            # Check if ValueError raised on parse
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", file1, file2])


class TestFileIsNotWritableAction(ActionHeroTestCase):
    def test_on_writable_file(self):
        self.parser.add_argument("--path", action=FileIsNotWritableAction)
        # Specify file
        with tempfile.NamedTemporaryFile() as file1:
            # Assert file is writable
            self.assertTrue(is_writable_file(file1.name))
            # Check if ValueError raised on parse
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", file1.name])

    def test_on_unwritable_file(self):
        self.parser.add_argument("--path", action=FileIsNotWritableAction)
        with tempfile.TemporaryDirectory() as dir1:
            # Specify file and remove write permission
            file1 = tempfile.mkstemp(dir=dir1)[1]
            remove_write_permission(file1)
            # Assert file is unwritable
            self.assertFalse(is_writable_file(file1))
            # No Error on parse args
            self.parser.parse_args(["--path", file1])
            # Assert file is unwritable
            self.assertFalse(is_writable_file(file1))

    def test_on_mixed_writable_and_unwritable_file(self):
        self.parser.add_argument(
            "--path", nargs="+", action=FileIsNotWritableAction
        )
        with tempfile.TemporaryDirectory() as dir1:
            # Specify writable and unwritable files
            file1 = tempfile.mkstemp(dir=dir1)[1]
            file2 = tempfile.mkstemp(dir=dir1)[1]
            remove_write_permission(file2)
            # Check if ValueError raised on parse
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", file1, file2])


class TestDirectoryIsWritableAction(ActionHeroTestCase):
    def test_on_writable_directory(self):
        self.parser.add_argument("--path", action=DirectoryIsWritableAction)
        # Specify writable directory
        with tempfile.TemporaryDirectory() as dir1:
            # Parse with readable directory
            self.parser.parse_args(["--path", dir1])

    def test_on_wunwritable_directory(self):
        self.parser.add_argument("--path", action=DirectoryIsWritableAction)
        with tempfile.TemporaryDirectory() as dir1:
            # Specify unwritable directory and remove write permissions
            dir2 = tempfile.mkdtemp(dir=dir1)
            remove_write_permission(dir2)
            # Asserts error on parsing unwritable directory
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", dir2])

    def test_on_writable_and_unwritable_directories(self):
        self.parser.add_argument(
            "--path", nargs="+", action=DirectoryIsWritableAction
        )
        with tempfile.TemporaryDirectory() as dir1:
            # Specify unwritable directory and remove write permissions
            dir2 = tempfile.mkdtemp(dir=dir1)
            remove_write_permission(dir2)
            # Asserts error on parsing unwritable directory
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", dir1, dir2])


class TestDirectoryIsNotWritableAction(ActionHeroTestCase):
    def test_on_writable_directory(self):
        self.parser.add_argument("--path", action=DirectoryIsNotWritableAction)
        # Specify writable directory
        with tempfile.TemporaryDirectory() as dir1:
            # Asserts error on parsing unwritable directory
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", dir1])

    def test_on_unwritable_directory(self):
        self.parser.add_argument("--path", action=DirectoryIsNotWritableAction)
        with tempfile.TemporaryDirectory() as dir1:
            # Specify unwritable directory and remove write permissions
            dir2 = tempfile.mkdtemp(dir=dir1)
            remove_write_permission(dir2)
            # Parse with readable directory
            self.parser.parse_args(["--path", dir2])

    def test_on_writable_and_unwritable_directories(self):
        self.parser.add_argument(
            "--path", nargs="+", action=DirectoryIsNotWritableAction
        )
        with tempfile.TemporaryDirectory() as dir1:
            # Specify unwritable directory and remove write permissions
            dir2 = tempfile.mkdtemp(dir=dir1)
            remove_write_permission(dir2)
            # Asserts error on parsing unwritable directory
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", dir1, dir2])


class TestPathIsWritableAction(ActionHeroTestCase):
    def test_on_writable_directory(self):
        self.parser.add_argument("--path", action=PathIsWritableAction)
        # Specify writable directory
        with tempfile.TemporaryDirectory() as dir1:
            # Parse with readable directory
            self.parser.parse_args(["--path", dir1])

    def test_on_unwritable_directory(self):
        self.parser.add_argument("--path", action=PathIsWritableAction)
        with tempfile.TemporaryDirectory() as dir1:
            # Specify unwritable directory and remove write permissions
            dir2 = tempfile.mkdtemp(dir=dir1)
            remove_write_permission(dir2)
            # Asserts error on parsing unwritable directory
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", dir2])

    def test_on_writable_and_unwritable_directories(self):
        self.parser.add_argument(
            "--path", nargs="+", action=PathIsWritableAction
        )
        with tempfile.TemporaryDirectory() as dir1:
            # Specify unwritable directory and remove write permissions
            dir2 = tempfile.mkdtemp(dir=dir1)
            remove_write_permission(dir2)
            # Asserts error on parsing unwritable directory
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", dir1, dir2])


class TestPathIsNotWritableAction(ActionHeroTestCase):
    def test_on_writable_directory(self):
        self.parser.add_argument("--path", action=PathIsNotWritableAction)
        # Specify writable directory
        with tempfile.TemporaryDirectory() as dir1:
            # Asserts error on parsing unwritable directory
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", dir1])

    def test_on_unwritable_directory(self):
        self.parser.add_argument("--path", action=PathIsNotWritableAction)
        with tempfile.TemporaryDirectory() as dir1:
            # Specify unwritable directory and remove write permissions
            dir2 = tempfile.mkdtemp(dir=dir1)
            remove_write_permission(dir2)
            # Parse with readable directory
            self.parser.parse_args(["--path", dir2])

    def test_on_writable_and_unwritable_directories(self):
        self.parser.add_argument(
            "--path", nargs="+", action=PathIsNotWritableAction
        )
        with tempfile.TemporaryDirectory() as dir1:
            # Specify unwritable directory and remove write permissions
            dir2 = tempfile.mkdtemp(dir=dir1)
            remove_write_permission(dir2)
            # Asserts error on parsing unwritable directory
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", dir1, dir2])


class TestFileIsReadableAction(ActionHeroTestCase):
    def test_on_readable_file(self):
        self.parser.add_argument("--path", action=FileIsReadableAction)
        # Specify file
        with tempfile.NamedTemporaryFile() as file1:
            # Assert file is readable
            self.assertTrue(is_readable_file(file1.name))
            # No errors when parsing args
            self.parser.parse_args(["--path", file1.name])
            # Assert file is still readable
            self.assertTrue(is_readable_file(file1.name))

    def test_on_unreadable_file(self):
        self.parser.add_argument("--path", action=FileIsReadableAction)
        # Specify file
        with tempfile.NamedTemporaryFile() as file1:
            # Assert file is readable
            self.assertTrue(is_readable_file(file1.name))
            # No errors when parsing args
            self.parser.parse_args(["--path", file1.name])

    def test_on_mixed_readable_and_unreadable_file(self):
        self.parser.add_argument(
            "--path", nargs="+", action=FileIsReadableAction
        )
        with tempfile.TemporaryDirectory() as dir1:
            # Specify readable and unreadable file
            file1 = tempfile.mkstemp(dir=dir1)[1]
            file2 = tempfile.mkstemp(dir=dir1)[1]
            remove_read_permission(file2)
            # Check if ValueError raised on parse
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", file1, file2])


class TestFileIsNotReadableAction(ActionHeroTestCase):
    def test_on_readable_file(self):
        self.parser.add_argument("--path", action=FileIsNotReadableAction)
        # Specify file
        with tempfile.NamedTemporaryFile() as file1:
            # Assert file is readable
            self.assertTrue(is_readable_file(file1.name))
            # Check if ValueError raised on parse
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", file1.name])

    def test_on_unreadable_file(self):
        self.parser.add_argument("--path", action=FileIsNotReadableAction)
        with tempfile.TemporaryDirectory() as dir1:
            # Specify file and remove write permission
            file1 = tempfile.mkstemp(dir=dir1)[1]
            remove_read_permission(file1)
            # Assert file is unreadable
            self.assertFalse(is_readable_file(file1))
            # No Error on parse args
            self.parser.parse_args(["--path", file1])
            # Assert file is unreadable
            self.assertFalse(is_readable_file(file1))

    def test_on_mixed_readable_and_unreadable_file(self):
        self.parser.add_argument(
            "--path", nargs="+", action=FileIsNotReadableAction
        )
        with tempfile.TemporaryDirectory() as dir1:
            # Specify readable and unreadable files
            file1 = tempfile.mkstemp(dir=dir1)[1]
            file2 = tempfile.mkstemp(dir=dir1)[1]
            remove_write_permission(file2)
            # Check if ValueError raised on parse
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", file1, file2])


class TestDirectoryIsReadableAction(ActionHeroTestCase):
    def test_on_readable_directory(self):
        self.parser.add_argument("--path", action=DirectoryIsReadableAction)
        # Specify directory
        with tempfile.TemporaryDirectory() as dir1:
            # Assert directory is readable
            self.assertTrue(is_readable_directory(dir1))
            # No errors when parsing args
            self.parser.parse_args(["--path", dir1])
            # Assert directory is still readable
            self.assertTrue(is_readable_directory(dir1))

    def test_on_unreadable_directory(self):
        self.parser.add_argument("--path", action=DirectoryIsReadableAction)
        # Specify dir amd make unreadable
        dir1 = tempfile.mkdtemp()
        remove_read_permission(dir1)
        # Assert ValueError raised when parsing args
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--path", dir1])
        # Tear down temp dirs
        os.rmdir(dir1)

    def test_on_mixed_readable_and_unreadable_directories(self):
        self.parser.add_argument(
            "--path", nargs="+", action=DirectoryIsReadableAction
        )
        # Specify readable and unreadable dirs
        with tempfile.TemporaryDirectory() as dir1:
            dir2 = tempfile.mkdtemp()
            remove_read_permission(dir2)
            # Assert ValueError raised when parsing args
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", dir1, dir2])


class TestDirectoryIsNotReadableAction(ActionHeroTestCase):
    def test_on_readable_directory(self):
        self.parser.add_argument("--path", action=DirectoryIsNotReadableAction)
        # Specify directory
        with tempfile.TemporaryDirectory() as dir1:
            # Assert directory is readable
            self.assertTrue(is_readable_directory(dir1))
            # Assert ValueError raised when parsing args
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", dir1])

    def test_on_unreadable_directory(self):
        self.parser.add_argument("--path", action=DirectoryIsNotReadableAction)
        # Specify dir amd make unreadable
        dir1 = tempfile.mkdtemp()
        remove_read_permission(dir1)
        # No errors when parsing args
        self.parser.parse_args(["--path", dir1])
        # Assert directory is still unreadable
        self.assertFalse(is_readable_directory(dir1))
        # Tear down temp dirs
        os.rmdir(dir1)

    def test_on_mixed_readable_and_unreadable_directories(self):
        self.parser.add_argument(
            "--path", nargs="+", action=DirectoryIsNotReadableAction
        )
        # Specify readable and unreadable dirs
        with tempfile.TemporaryDirectory() as dir1:
            dir2 = tempfile.mkdtemp()
            remove_read_permission(dir2)
            # Assert ValueError raised when parsing args
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", dir1, dir2])


class TestPathIsReadableAction(ActionHeroTestCase):
    def test_on_readable_file(self):
        self.parser.add_argument("--path", action=PathIsReadableAction)
        # Specify file
        with tempfile.NamedTemporaryFile() as file1:
            # Assert file is readable
            self.assertTrue(is_readable_file(file1.name))
            # No errors when parsing args
            self.parser.parse_args(["--path", file1.name])
            # Assert file is still readable
            self.assertTrue(is_readable_file(file1.name))

    def test_on_unreadable_file(self):
        self.parser.add_argument("--path", action=PathIsReadableAction)
        # Specify file
        with tempfile.NamedTemporaryFile() as file1:
            # Assert file is readable
            self.assertTrue(is_readable_file(file1.name))
            # No errors when parsing args
            self.parser.parse_args(["--path", file1.name])

    def test_on_mixed_readable_and_unreadable_file(self):
        self.parser.add_argument(
            "--path", nargs="+", action=PathIsReadableAction
        )
        with tempfile.TemporaryDirectory() as dir1:
            # Specify readable and unreadable file
            file1 = tempfile.mkstemp(dir=dir1)[1]
            file2 = tempfile.mkstemp(dir=dir1)[1]
            remove_read_permission(file2)
            # Check if ValueError raised on parse
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", file1, file2])

    def test_on_readable_directory(self):
        self.parser.add_argument("--path", action=PathIsReadableAction)
        # Specify directory
        with tempfile.TemporaryDirectory() as dir1:
            # Assert directory is readable
            self.assertTrue(is_readable_directory(dir1))
            # No errors when parsing args
            self.parser.parse_args(["--path", dir1])
            # Assert directory is still readable
            self.assertTrue(is_readable_directory(dir1))

    def test_on_unreadable_directory(self):
        self.parser.add_argument("--path", action=PathIsReadableAction)
        # Specify dir amd make unreadable
        dir1 = tempfile.mkdtemp()
        remove_read_permission(dir1)
        # Assert ValueError raised when parsing args
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--path", dir1])
        # Tear down temp dirs
        os.rmdir(dir1)

    def test_on_mixed_readable_and_unreadable_directories(self):
        self.parser.add_argument(
            "--path", nargs="+", action=PathIsReadableAction
        )
        # Specify readable and unreadable dirs
        with tempfile.TemporaryDirectory() as dir1:
            dir2 = tempfile.mkdtemp()
            remove_read_permission(dir2)
            # Assert ValueError raised when parsing args
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", dir1, dir2])


class TestPathIsNotReadableAction(ActionHeroTestCase):
    def test_on_readable_file(self):
        self.parser.add_argument("--path", action=PathIsNotReadableAction)
        # Specify file
        with tempfile.NamedTemporaryFile() as file1:
            # Assert file is readable
            self.assertTrue(is_readable_file(file1.name))
            # Check if ValueError raised on parse
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", file1.name])

    def test_on_unreadable_file(self):
        self.parser.add_argument("--path", action=PathIsNotReadableAction)
        with tempfile.TemporaryDirectory() as dir1:
            # Specify file and remove write permission
            file1 = tempfile.mkstemp(dir=dir1)[1]
            remove_read_permission(file1)
            # Assert file is unreadable
            self.assertFalse(is_readable_file(file1))
            # No Error on parse args
            self.parser.parse_args(["--path", file1])
            # Assert file is unreadable
            self.assertFalse(is_readable_path(file1))

    def test_on_mixed_readable_and_unreadable_file(self):
        self.parser.add_argument(
            "--path", nargs="+", action=PathIsNotReadableAction
        )
        with tempfile.TemporaryDirectory() as dir1:
            # Specify readable and unreadable files
            file1 = tempfile.mkstemp(dir=dir1)[1]
            file2 = tempfile.mkstemp(dir=dir1)[1]
            remove_write_permission(file2)
            # Check if ValueError raised on parse
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", file1, file2])

    def test_on_readable_directory(self):
        self.parser.add_argument("--path", action=PathIsNotReadableAction)
        # Specify directory
        with tempfile.TemporaryDirectory() as dir1:
            # Assert directory is readable
            self.assertTrue(is_readable_directory(dir1))
            # Assert ValueError raised when parsing args
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", dir1])

    def test_on_unreadable_directory(self):
        self.parser.add_argument("--path", action=PathIsNotReadableAction)
        # Specify dir amd make unreadable
        dir1 = tempfile.mkdtemp()
        remove_read_permission(dir1)
        # No errors when parsing args
        self.parser.parse_args(["--path", dir1])
        # Assert directory is still unreadable
        self.assertFalse(is_readable_directory(dir1))
        # Tear down temp dirs
        os.rmdir(dir1)

    def test_on_mixed_readable_and_unreadable_directories(self):
        self.parser.add_argument(
            "--path", nargs="+", action=PathIsNotReadableAction
        )
        # Specify readable and unreadable dirs
        with tempfile.TemporaryDirectory() as dir1:
            dir2 = tempfile.mkdtemp()
            remove_read_permission(dir2)
            # Assert ValueError raised when parsing args
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", dir1, dir2])


class TestFileIsExecutableAction(ActionHeroTestCase):
    def test_on_executable_file(self):
        self.parser.add_argument("--path", action=FileIsExecutableAction)
        # Specify file and make executable
        with tempfile.NamedTemporaryFile() as file1:
            add_execute_permission(file1.name)
            self.assertTrue(is_executable_file(file1.name))
            # No errors when parsing args
            self.parser.parse_args(["--path", file1.name])

    def test_on_unexecutable_file(self):
        self.parser.add_argument("--path", action=FileIsExecutableAction)
        # Specify file and assert not executable
        with tempfile.NamedTemporaryFile() as file1:
            self.assertFalse(is_executable_file(file1.name))
            # Assert ValueError on parsing
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", file1.name])

    def test_on_mixed_executable_and_unexecutable_file(self):
        self.parser.add_argument(
            "--path", nargs="+", action=FileIsExecutableAction
        )
        with tempfile.TemporaryDirectory() as dir1:
            # Specify readable and unreadable file
            file1 = tempfile.mkstemp(dir=dir1)[1]
            file2 = tempfile.mkstemp(dir=dir1)[1]
            add_execute_permission(file2)
            # Check if ValueError raised on parse
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", file1, file2])


class TestFileIsNotExecutableAction(ActionHeroTestCase):
    def test_on_executable_file(self):
        self.parser.add_argument("--path", action=FileIsNotExecutableAction)
        # Specify file and make executable
        with tempfile.NamedTemporaryFile() as file1:
            add_execute_permission(file1.name)
            self.assertTrue(is_executable_file(file1.name))
            # Check if ValueError raised on parse
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", file1.name])

    def test_on_unreadable_file(self):
        self.parser.add_argument("--path", action=FileIsNotExecutableAction)
        with tempfile.TemporaryDirectory() as dir1:
            # Specify file and remove write permission
            file1 = tempfile.mkstemp(dir=dir1)[1]
            # Assert file is unexecutable
            self.assertFalse(is_executable_file(file1))
            # No Error on parse args
            self.parser.parse_args(["--path", file1])
            # Assert file is unexecutable
            self.assertFalse(is_executable_file(file1))

    def test_on_mixed_executable_and_unexecutable_file(self):
        self.parser.add_argument(
            "--path", nargs="+", action=FileIsNotExecutableAction
        )
        with tempfile.TemporaryDirectory() as dir1:
            # Specify executable and unexecutable files
            file1 = tempfile.mkstemp(dir=dir1)[1]
            add_execute_permission(file1)
            file2 = tempfile.mkstemp(dir=dir1)[1]
            # Check if ValueError raised on parse
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", file1, file2])


class TestDirectoryIsExecutableAction(ActionHeroTestCase):
    def test_on_executable_directory(self):
        self.parser.add_argument("--path", action=DirectoryIsExecutableAction)
        # Specify directory and make executable
        with tempfile.TemporaryDirectory() as dir1:
            self.assertTrue(is_executable_directory(dir1))
            # No errors when parsing args
            self.parser.parse_args(["--path", dir1])

    def test_on_unexecutable_directory(self):
        self.parser.add_argument("--path", action=DirectoryIsExecutableAction)
        # Specify dir and make unexecutable
        with tempfile.TemporaryDirectory() as dir1:
            remove_execute_permission(dir1)
            # Assert ValueError raised when parsing args
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", dir1])

    def test_on_mixed_executable_and_unexecutable_directories(self):
        self.parser.add_argument(
            "--path", nargs="+", action=DirectoryIsExecutableAction
        )
        # Specify executable and unexecutable dirs
        with tempfile.TemporaryDirectory() as dir1:
            dir2 = tempfile.mkdtemp()
            remove_execute_permission(dir2)
            # Assert ValueError raised when parsing args
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", dir1, dir2])


class TestDirectoryIsNotExecutableAction(ActionHeroTestCase):
    def test_on_executable_directory(self):
        self.parser.add_argument(
            "--path", action=DirectoryIsNotExecutableAction
        )
        # Specify directory
        with tempfile.TemporaryDirectory() as dir1:
            # Assert directory is executable
            self.assertTrue(is_executable_directory(dir1))
            # Assert ValueError raised when parsing args
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", dir1])

    def test_on_unexecutable_directory(self):
        self.parser.add_argument(
            "--path", action=DirectoryIsNotExecutableAction
        )
        # Specify dir amd make unexecutable
        with tempfile.TemporaryDirectory() as dir1:
            dir1 = tempfile.mkdtemp()
            remove_execute_permission(dir1)
            # No errors when parsing args
            self.parser.parse_args(["--path", dir1])
            # Assert directory is still unreadable
            self.assertFalse(is_executable_directory(dir1))

    def test_on_mixed_executable_and_unexecutable_directories(self):
        self.parser.add_argument(
            "--path", nargs="+", action=DirectoryIsNotExecutableAction
        )
        # Specify executable and unexecutable dirs
        with tempfile.TemporaryDirectory() as dir1:
            dir2 = tempfile.mkdtemp()
            remove_execute_permission(dir2)
            # Assert ValueError raised when parsing args
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", dir1, dir2])


class TestPathIsExecutableAction(ActionHeroTestCase):
    def test_on_executable_file(self):
        self.parser.add_argument("--path", action=PathIsExecutableAction)
        # Specify file and make executable
        with tempfile.NamedTemporaryFile() as file1:
            add_execute_permission(file1.name)
            self.assertTrue(is_executable_file(file1.name))
            # No errors when parsing args
            self.parser.parse_args(["--path", file1.name])

    def test_on_unexecutable_file(self):
        self.parser.add_argument("--path", action=PathIsExecutableAction)
        # Specify file and assert not executable
        with tempfile.NamedTemporaryFile() as file1:
            self.assertFalse(is_executable_file(file1.name))
            # Assert ValueError on parsing
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", file1.name])

    def test_on_mixed_executable_and_unexecutable_file(self):
        self.parser.add_argument(
            "--path", nargs="+", action=PathIsExecutableAction
        )
        with tempfile.TemporaryDirectory() as dir1:
            # Specify readable and unreadable file
            file1 = tempfile.mkstemp(dir=dir1)[1]
            file2 = tempfile.mkstemp(dir=dir1)[1]
            add_execute_permission(file2)
            # Check if ValueError raised on parse
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", file1, file2])

    def test_on_executable_directory(self):
        self.parser.add_argument("--path", action=PathIsExecutableAction)
        # Specify directory and make executable
        with tempfile.TemporaryDirectory() as dir1:
            self.assertTrue(is_executable_directory(dir1))
            # No errors when parsing args
            self.parser.parse_args(["--path", dir1])

    def test_on_unexecutable_directory(self):
        self.parser.add_argument("--path", action=PathIsExecutableAction)
        # Specify dir and make unexecutable
        with tempfile.TemporaryDirectory() as dir1:
            remove_execute_permission(dir1)
            # Assert ValueError raised when parsing args
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", dir1])

    def test_on_mixed_executable_and_unexecutable_directories(self):
        self.parser.add_argument(
            "--path", nargs="+", action=PathIsExecutableAction
        )
        # Specify executable and unexecutable dirs
        with tempfile.TemporaryDirectory() as dir1:
            dir2 = tempfile.mkdtemp()
            remove_execute_permission(dir2)
            # Assert ValueError raised when parsing args
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", dir1, dir2])


class TestPathIsNotExecutableAction(ActionHeroTestCase):
    def test_on_executable_file(self):
        self.parser.add_argument("--path", action=PathIsNotExecutableAction)
        # Specify file and make executable
        with tempfile.NamedTemporaryFile() as file1:
            add_execute_permission(file1.name)
            self.assertTrue(is_executable_file(file1.name))
            # Check if ValueError raised on parse
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", file1.name])

    def test_on_unreadable_file(self):
        self.parser.add_argument("--path", action=PathIsNotExecutableAction)
        with tempfile.TemporaryDirectory() as dir1:
            # Specify file and remove write permission
            file1 = tempfile.mkstemp(dir=dir1)[1]
            # Assert file is unexecutable
            self.assertFalse(is_executable_file(file1))
            # No Error on parse args
            self.parser.parse_args(["--path", file1])
            # Assert file is unexecutable
            self.assertFalse(is_executable_file(file1))

    def test_on_mixed_executable_and_unexecutable_file(self):
        self.parser.add_argument(
            "--path", nargs="+", action=PathIsNotExecutableAction
        )
        with tempfile.TemporaryDirectory() as dir1:
            # Specify executable and unexecutable files
            file1 = tempfile.mkstemp(dir=dir1)[1]
            add_execute_permission(file1)
            file2 = tempfile.mkstemp(dir=dir1)[1]
            # Check if ValueError raised on parse
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", file1, file2])

    def test_on_executable_directory(self):
        self.parser.add_argument("--path", action=PathIsNotExecutableAction)
        # Specify directory
        with tempfile.TemporaryDirectory() as dir1:
            # Assert directory is executable
            self.assertTrue(is_executable_directory(dir1))
            # Assert ValueError raised when parsing args
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", dir1])

    def test_on_unexecutable_directory(self):
        self.parser.add_argument("--path", action=PathIsNotExecutableAction)
        # Specify dir amd make unexecutable
        with tempfile.TemporaryDirectory() as dir1:
            dir1 = tempfile.mkdtemp()
            remove_execute_permission(dir1)
            # No errors when parsing args
            self.parser.parse_args(["--path", dir1])
            # Assert directory is still unreadable
            self.assertFalse(is_executable_directory(dir1))

    def test_on_mixed_executable_and_unexecutable_directories(self):
        self.parser.add_argument(
            "--path", nargs="+", action=PathIsNotExecutableAction
        )
        # Specify executable and unexecutable dirs
        with tempfile.TemporaryDirectory() as dir1:
            dir2 = tempfile.mkdtemp()
            remove_execute_permission(dir2)
            # Assert ValueError raised when parsing args
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", dir1, dir2])


class TestFileIsEmptyAction(ActionHeroTestCase):
    def test_on_empty_file(self):
        self.parser.add_argument("--path", action=FileIsEmptyAction)
        with tempfile.NamedTemporaryFile() as file1:
            self.assertTrue(is_empty_file(file1.name))
            self.parser.parse_args(["--path", file1.name])

    def test_on_nonempty_file(self):
        self.parser.add_argument("--path", action=FileIsEmptyAction)
        with tempfile.NamedTemporaryFile() as file1:
            with open(file1.name, "a") as file_for_writing:
                file_for_writing.write("SOME TEXT")
            self.assertFalse(is_empty_file(file1.name))
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", file1.name])

    def test_on_list_of_empty_and_nonempty_files(self):
        self.parser.add_argument("--path", nargs="+", action=FileIsEmptyAction)
        with tempfile.NamedTemporaryFile() as file1:
            with tempfile.NamedTemporaryFile() as file2:
                with open(file2.name, "a") as file_for_writing:
                    file_for_writing.write("SOME TEXT")
                self.assertTrue(is_empty_file(file1.name))
                self.assertFalse(is_empty_file(file2.name))
                with self.assertRaises(ValueError):
                    self.parser.parse_args(["--path", file1.name, file2.name])


class TestFileIsNotEmptyAction(ActionHeroTestCase):
    def test_on_empty_file(self):
        self.parser.add_argument("--path", action=FileIsNotEmptyAction)
        with tempfile.NamedTemporaryFile() as file1:
            self.assertTrue(is_empty_file(file1.name))
            with self.assertRaises(ValueError):
                self.parser.parse_args(["--path", file1.name])

    def test_on_nonempty_file(self):
        self.parser.add_argument("--path", action=FileIsNotEmptyAction)
        with tempfile.NamedTemporaryFile() as file1:
            with open(file1.name, "a") as file_for_writing:
                file_for_writing.write("SOME TEXT")
            self.assertFalse(is_empty_file(file1.name))
            self.parser.parse_args(["--path", file1.name])

    def test_on_list_of_empty_and_nonempty_files(self):
        self.parser.add_argument(
            "--path", nargs="+", action=FileIsNotEmptyAction
        )
        with tempfile.NamedTemporaryFile() as file1:
            with tempfile.NamedTemporaryFile() as file2:
                with open(file2.name, "a") as file_for_writing:
                    file_for_writing.write("SOME TEXT")
                self.assertTrue(is_empty_file(file1.name))
                self.assertFalse(is_empty_file(file2.name))
                with self.assertRaises(ValueError):
                    self.parser.parse_args(["--path", file1.name, file2.name])


class TestFilenameHasExtension(ActionHeroTestCase):
    def test_on_parser_with_extension(self):
        self.parser.add_argument(
            "--filename", action=FilenameHasExtension, action_values=["txt"]
        )

    def test_on_parser_without_extension(self):
        with self.assertRaises(ValueError):
            self.parser.add_argument("--filename", action=FilenameHasExtension)

    def test_on_filename_with_matching_extension(self):
        self.parser.add_argument(
            "--filename", action=FilenameHasExtension, action_values=["txt"]
        )
        self.parser.parse_args(["--filename", "diary.txt"])

    def test_on_filename_with_nonmatching_extension(self):
        self.parser.add_argument(
            "--filename", action=FilenameHasExtension, action_values=["txt"]
        )
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--filename", "diary.md"])

    def test_on_list_of_filenames_with_matching_extension(self):
        self.parser.add_argument(
            "--filename",
            nargs="+",
            action=FilenameHasExtension,
            action_values=["txt"],
        )
        self.parser.parse_args(
            ["--filename", "diary.txt", "log.txt", "lyrics.txt"]
        )

    def test_on_list_of_filenames_with_nonmatching_extension(self):
        self.parser.add_argument(
            "--filename",
            nargs="+",
            action=FilenameHasExtension,
            action_values=["txt"],
        )
        with self.assertRaises(ValueError):
            self.parser.parse_args(
                ["--filename", "diary.md", "README.rst", "history.sh"]
            )

    def test_on_list_of_filenames_with_mixed_matching_extensions(self):
        self.parser.add_argument(
            "--filename",
            nargs="+",
            action=FilenameHasExtension,
            action_values=["txt"],
        )
        with self.assertRaises(ValueError):
            self.parser.parse_args(
                [
                    "--filename",
                    "notes.txt",
                    "diary.md",
                    "README.rst",
                    "history.sh",
                ]
            )

    def test_on_multiple_action_values(self):
        self.parser.add_argument(
            "--filename",
            action=FilenameHasExtension,
            action_values=["md", "markdown"],
        )
        self.parser.parse_args(["--filename", "diary.md"])

    def test_on_multiple_action_values_with_expected_filenames(self):
        self.parser.add_argument(
            "--filename",
            action=FilenameHasExtension,
            action_values=["md", "markdown"],
        )
        with self.assertRaises(ValueError):
            self.parser.parse_args(
                ["--filename", "README.md", "blogentry.markdown"]
            )

    def test_on_multiple_action_values_with_unexpected_filenames(self):
        self.parser.add_argument(
            "--filename",
            action=FilenameHasExtension,
            action_values=["md", "markdown"],
        )
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--filename", "config.yml"])

    def test_on_multiple_action_values_with_mixed_expected_filenames(self):
        self.parser.add_argument(
            "--filename",
            nargs="+",
            action=FilenameHasExtension,
            action_values=["md", "markdown"],
        )
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--filename", "config.yml", "README.rst"])
