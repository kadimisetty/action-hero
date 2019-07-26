import unittest
import pathlib
import tempfile
import shutil
import stat
import os

from action_heroes.path_utils import (
    get_extension,
    create_directory,
    create_file,
    is_executable_directory,
    is_executable_file,
    is_executable_path,
    is_existing_directory,
    is_existing_file,
    is_existing_or_creatable_path,
    is_existing_path,
    is_readable_directory,
    is_readable_file,
    is_readable_path,
    is_symbolic_link,
    is_valid_directory,
    is_valid_file,
    is_valid_path,
    is_writable_directory,
    is_writable_file,
    is_writable_path,
    resolve_path,
)


class TestExistenceUtils(unittest.TestCase):
    def test_is_existing_directory_on_exisiting_directory(self):
        with tempfile.TemporaryDirectory() as dir1:
            self.assertTrue(is_existing_directory(dir1))

    def test_is_existing_directory_on_nonexisting_directory(self):
        dir1 = tempfile.mkdtemp()
        os.rmdir(dir1)

        self.assertFalse(is_existing_directory(dir1))

    def test_is_existing_file_on_exisiting_file(self):
        with tempfile.NamedTemporaryFile() as file1:
            self.assertTrue(is_existing_file(file1.name))

    def test_is_existing_file_on_nonexisting_file(self):
        # Create and Remove a file to confirm it doesnt exist
        file1 = tempfile.mkstemp()[1]
        os.remove(file1)

        self.assertFalse(is_existing_file(file1))

    def test_is_existing_path_on_exisiting_file(self):
        with tempfile.NamedTemporaryFile() as file1:
            self.assertTrue(is_existing_path(file1.name))

    def test_is_existing_path_on_nonexisting_file(self):
        # Create and Remove a file to confirm it doesnt exist
        file1 = tempfile.mkstemp()[1]
        os.remove(file1)

        self.assertFalse(is_existing_path(file1))

    def test_is_existing_path_on_exisiting_directory(self):
        with tempfile.TemporaryDirectory() as dir1:
            self.assertTrue(is_existing_path(dir1))

    def test_is_existing_path_on_nonexisting_directory(self):
        # Create and Remove a directory to confirm it doesnt exist
        dir1 = tempfile.mkdtemp()
        os.rmdir(dir1)

        self.assertFalse(is_existing_path(dir1))


class TestWritableUtils(unittest.TestCase):
    @staticmethod
    def _remove_write_permission(path):
        """Remove write permissions and keep other permissions intact.

        Params:
            path:  The path whose permissions to alter.

        Source:
            https://stackoverflow.com/a/38511116/225903

        """
        NO_USER_WRITING = ~stat.S_IWUSR
        NO_GROUP_WRITING = ~stat.S_IWGRP
        NO_OTHER_WRITING = ~stat.S_IWOTH
        NO_WRITING = NO_USER_WRITING & NO_GROUP_WRITING & NO_OTHER_WRITING

        current_permissions = stat.S_IMODE(os.lstat(path).st_mode)
        os.chmod(path, current_permissions & NO_WRITING)

    def test_is_writable_directory_on_writable_directory(self):
        with tempfile.TemporaryDirectory() as dir1:
            self.assertTrue(is_writable_directory(dir1))

    def test_is_writable_directory_on_unwritable_directory(self):
        with tempfile.TemporaryDirectory() as dir1:
            self._remove_write_permission(dir1)
            self.assertFalse(is_writable_directory(dir1))

    def test_is_writable_file_on_writable_file(self):
        with tempfile.NamedTemporaryFile() as file1:
            self.assertTrue(is_writable_file(file1.name))

    def test_is_writable_file_on_unwritable_file(self):
        with tempfile.NamedTemporaryFile() as file1:
            self._remove_write_permission(file1.name)
            self.assertFalse(is_writable_file(file1.name))

    def test_is_writable_path_on_writable_directory(self):
        with tempfile.TemporaryDirectory() as dir1:
            self.assertTrue(is_writable_path(dir1))

    def test_is_writable_path_on_unwritable_directory(self):
        with tempfile.TemporaryDirectory() as dir1:
            self._remove_write_permission(dir1)
            self.assertFalse(is_writable_path(dir1))

    def test_is_writable_path_on_writable_file(self):
        with tempfile.NamedTemporaryFile() as file1:
            self.assertTrue(is_writable_path(file1.name))

    def test_is_writable_path_on_unwritable_file(self):
        with tempfile.NamedTemporaryFile() as file1:
            self._remove_write_permission(file1.name)
            self.assertFalse(is_writable_path(file1.name))


@unittest.skip
class TestReadableUtils(unittest.TestCase):
    @staticmethod
    def _remove_read_permissions(path):
        """Remove read permissions and keep other permissions intact.

        Params:
            path:  The path whose permissions to alter.

        Source:
            https://stackoverflow.com/a/38511116/225903

        """
        NO_USER_READING = ~stat.S_IRUSR
        NO_GROUP_READING = ~stat.S_IRGRP
        NO_OTHER_READING = ~stat.S_IROTH
        NO_READING = NO_USER_READING & NO_GROUP_READING & NO_OTHER_READING

        current_permissions = stat.S_IMODE(os.lstat(path).st_mode)
        os.chmod(path, current_permissions & NO_READING)

    def test_is_readable_directory_on_readable_directory(self):
        with tempfile.TemporaryDirectory() as dir1:
            self.assertTrue(is_readable_directory(dir1))

    def test_is_readable_directory_on_unreadable_directory(self):
        with tempfile.TemporaryDirectory() as dir1:
            self._remove_read_permissions(dir1)
            self.assertFalse(is_readable_directory(dir1))

    def test_is_readable_file_on_readable_file(self):
        with tempfile.NamedTemporaryFile() as file1:
            self.assertTrue(is_readable_file(file1.name))

    def test_is_readable_file_on_unreadable_file(self):
        with tempfile.NamedTemporaryFile() as file1:
            self._remove_read_permissions(file1.name)
            self.assertFalse(is_readable_file(file1.name))

    def test_is_readable_path_on_readable_directory(self):
        with tempfile.TemporaryDirectory() as dir1:
            self.assertTrue(is_readable_path(dir1))

    def test_is_readable_path_on_unreadable_directory(self):
        with tempfile.TemporaryDirectory() as dir1:
            self._remove_read_permissions(dir1)
            self.assertFalse(is_readable_path(dir1))

    def test_is_readable_path_on_readable_file(self):
        with tempfile.NamedTemporaryFile() as file1:
            self.assertTrue(is_readable_path(file1.name))

    def test_is_readable_path_on_unreadable_file(self):
        with tempfile.NamedTemporaryFile() as file1:
            self._remove_read_permissions(file1.name)
            self.assertFalse(is_readable_path(file1.name))


class TestExecutableUtils(unittest.TestCase):
    @staticmethod
    def _remove_execute_permissions(path):
        """Remove execute permissions and keep other permissions intact.

        Params:
            path:  The path whose permissions to alter.

        Source:
            https://stackoverflow.com/a/38511116/225903

        """
        NO_USER_EXECUTING = ~stat.S_IXUSR
        NO_GROUP_EXECUTING = ~stat.S_IXGRP
        NO_OTHER_EXECUTING = ~stat.S_IXOTH
        NO_EXECUTING = (
            NO_USER_EXECUTING & NO_GROUP_EXECUTING & NO_OTHER_EXECUTING
        )

        current_permissions = stat.S_IMODE(os.lstat(path).st_mode)
        os.chmod(path, current_permissions & NO_EXECUTING)

    @staticmethod
    def _add_execute_permissions(path):
        """Add execute permissions and keep other permissions intact.

        Params:
            path:  The path whose permissions to alter.

        Source:
            https://stackoverflow.com/a/38511116/225903

        """
        USER_EXECUTING = stat.S_IXUSR
        GROUP_EXECUTING = stat.S_IXGRP
        OTHER_EXECUTING = stat.S_IXOTH
        EXECUTING = USER_EXECUTING | GROUP_EXECUTING | OTHER_EXECUTING

        current_permissions = stat.S_IMODE(os.lstat(path).st_mode)
        os.chmod(path, current_permissions | EXECUTING)

    def test_is_executable_directory_on_executable_directory(self):
        with tempfile.TemporaryDirectory() as dir1:
            self.assertTrue(is_executable_directory(dir1))

    def test_is_executable_directory_on_unexecutable_directory(self):
        with tempfile.TemporaryDirectory() as dir1:
            self._remove_execute_permissions(dir1)
            self.assertFalse(is_executable_directory(dir1))

    def test_is_executable_file_on_executable_file(self):
        with tempfile.NamedTemporaryFile() as file1:
            self._add_execute_permissions(file1.name)
            self.assertTrue(is_executable_file(file1.name))

    def test_is_executable_file_on_unexecutable_file(self):
        with tempfile.NamedTemporaryFile() as file1:
            self._remove_execute_permissions(file1.name)
            self.assertFalse(is_executable_file(file1.name))

    def test_is_executable_path_on_executable_directory(self):
        with tempfile.TemporaryDirectory() as dir1:
            self.assertTrue(is_executable_path(dir1))

    def test_is_executable_path_on_unexecutable_directory(self):
        with tempfile.TemporaryDirectory() as dir1:
            self._remove_execute_permissions(dir1)
            self.assertFalse(is_executable_path(dir1))

    def test_is_executable_path_on_executable_file(self):
        with tempfile.NamedTemporaryFile() as file1:
            self._add_execute_permissions(file1.name)
            self.assertTrue(is_executable_path(file1.name))

    def test_is_executable_path_on_unexecutable_file(self):
        with tempfile.NamedTemporaryFile() as file1:
            self.assertFalse(is_executable_path(file1.name))


class TestSymbolicLinkUtils(unittest.TestCase):
    def setUp(self):
        # Create parent directory to hold symbolic links
        self.parent_directory = tempfile.mkdtemp()

        # Create temporary directory and a symbolic link pointing to it
        self.dir1 = tempfile.mkdtemp()
        self.link_to_dir1 = os.path.join(
            self.parent_directory, os.path.basename(self.dir1)
        )
        os.symlink(
            src=self.dir1,
            dst=self.link_to_dir1,
            target_is_directory=True,
        )

        # Create temporary file and a symbolic link pointing to it
        self.file1 = tempfile.mkstemp()[1]
        self.link_to_file1 = os.path.join(
            self.parent_directory, os.path.basename(self.file1)
        )
        os.symlink(src=self.file1, dst=self.link_to_file1)

    def tearDown(self):
        # Unlink symbolic links
        os.unlink(self.link_to_file1)
        os.unlink(self.link_to_dir1)

        # Remove temporary directories and file
        shutil.rmtree(self.parent_directory)
        os.rmdir(self.dir1)
        os.remove(self.file1)

    def test_is_symbolic_link_on_existing_link_to_directory(self):
        self.assertTrue(is_symbolic_link(self.link_to_dir1))

    def test_is_symbolic_link_on_existing_link_to_file(self):
        self.assertTrue(is_symbolic_link(self.link_to_file1))

    def test_is_symbolic_link_on_existing_directory(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            self.assertFalse(is_symbolic_link(temporary_directory))

    def test_is_symbolic_link_on_existing_file(self):
        with tempfile.NamedTemporaryFile() as temporary_file:
            self.assertFalse(is_symbolic_link(temporary_file.name))


class TestResolvePath(unittest.TestCase):
    def test_resolve_path_resolves_directory(self):
        with tempfile.TemporaryDirectory() as dir1:
            expected = os.path.realpath(dir1)
            self.assertEqual(resolve_path(dir1), expected)

    def test_resolve_path_resolves_file(self):
        with tempfile.NamedTemporaryFile() as file1:
            expected = os.path.realpath(file1.name)
            self.assertEqual(resolve_path(file1.name), expected)


class TestCreatePath(unittest.TestCase):
    def test_create_directory(self):
        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a directory in termporary directory
            dir1 = os.path.join(parent_directory, "SOMEDIR")
            create_directory(dir1)

            # Check if directory was created successfully
            self.assertTrue(os.path.isdir(dir1), True)

    def test_create_file(self):
        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a file in termporary directory
            file1 = os.path.join(parent_directory, "SOMEFILE")
            create_file(file1)

            # Check if file was created successfully
            self.assertTrue(os.path.isfile(file1), True)


class TestExistingOrCreatablePath(unittest.TestCase):
    def test_is_existing_or_creatable_path_on_existing_dir(self):
        with tempfile.TemporaryDirectory() as dir1:
            self.assertTrue(is_existing_or_creatable_path(dir1))

    def test_is_existing_or_creatable_path_on_nonexisting_creatable_dir(self):
        # Create and delete a temp directory so we know that it is a valid path
        dir1 = tempfile.mkdtemp()
        os.rmdir(dir1)
        self.assertTrue(is_existing_or_creatable_path(dir1))

    def test_is_existing_or_creatable_path_on_uncreatable_dir(self):
        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a directory name with a char forbidden in POSIX and WIN*
            forbidden_char = "/"
            directory_name = "SOMEDIR{}".format(forbidden_char)
            directory_path = os.path.join(parent_directory, directory_name)

            # Assert that the forbidden character prohibited path creation
            self.assertFalse(is_existing_or_creatable_path(directory_path))

    def test_is_existing_or_creatable_path_on_existing_file(self):
        with tempfile.NamedTemporaryFile() as file1:
            self.assertTrue(is_existing_or_creatable_path(file1.name))

    def test_is_existing_or_creatable_path_on_nonexisting_creatable_file(self):
        # Create and delete a temp file so we know that it is a valid path
        file1 = tempfile.mkstemp()[1]
        os.remove(file1)
        self.assertTrue(is_existing_or_creatable_path(file1))

    def test_is_existing_or_creatable_path_on_uncreatable_file(self):
        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a file name with a char forbidden in POSIX and WIN*
            forbidden_char = "/"
            file_name = "SOMEDIR{}".format(forbidden_char)
            file_path = os.path.join(parent_directory, file_name)

            # Assert that the forbidden character prohibited path creation
            self.assertFalse(is_existing_or_creatable_path(file_path))


class TestValidPath(unittest.TestCase):
    def test_is_valid_path_on_existing_dir(self):
        with tempfile.TemporaryDirectory() as dir1:
            self.assertTrue(is_valid_path(dir1))

    def test_is_valid_path_on_nonexisting_creatable_dir(self):
        # Create and delete a temp directory so we know that it is a valid path
        dir1 = tempfile.mkdtemp()
        os.rmdir(dir1)
        self.assertTrue(is_valid_path(dir1))

    def test_is_valid_path_on_uncreatable_dir(self):
        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a directory name with a char forbidden in POSIX and WIN*
            forbidden_char = "/"
            directory_name = "SOMEDIR{}".format(forbidden_char)
            directory_path = os.path.join(parent_directory, directory_name)

            # Assert that the forbidden character prohibited path creation
            self.assertFalse(is_valid_path(directory_path))

    def test_is_valid_path_on_existing_file(self):
        with tempfile.NamedTemporaryFile() as file1:
            self.assertTrue(is_valid_path(file1.name))

    def test_is_valid_path_on_nonexisting_creatable_file(self):
        # Create and delete a temp file so we know that it is a valid path
        file1 = tempfile.mkstemp()[1]
        os.remove(file1)
        self.assertTrue(is_valid_path(file1))

    def test_is_valid_path_on_uncreatable_file(self):
        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a file name with a char forbidden in POSIX and WIN*
            forbidden_char = "/"
            file_name = "SOMEDIR{}".format(forbidden_char)
            file_path = os.path.join(parent_directory, file_name)

            # Assert that the forbidden character prohibited path creation
            self.assertFalse(is_valid_path(file_path))


class TestValidDirectory(unittest.TestCase):
    def test_is_valid_path_on_existing_dir(self):
        with tempfile.TemporaryDirectory() as dir1:
            self.assertTrue(is_valid_directory(dir1))

    def test_is_valid_path_on_nonexisting_creatable_dir(self):
        # Create and delete a temp directory so we know that it is a valid path
        dir1 = tempfile.mkdtemp()
        os.rmdir(dir1)
        self.assertTrue(is_valid_directory(dir1))

    def test_is_valid_path_on_uncreatable_dir(self):
        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a directory name with a char forbidden in POSIX and WIN*
            forbidden_char = "/"
            directory_name = "SOMEDIR{}".format(forbidden_char)
            directory_path = os.path.join(parent_directory, directory_name)

            # Assert that the forbidden character prohibited path creation
            self.assertFalse(is_valid_directory(directory_path))


class TestValidFile(unittest.TestCase):
    def test_is_valid_path_on_existing_file(self):
        with tempfile.NamedTemporaryFile() as file1:
            self.assertTrue(is_valid_file(file1.name))

    def test_is_valid_path_on_nonexisting_creatable_file(self):
        # Create and delete a temp file so we know that it is a valid path
        file1 = tempfile.mkstemp()[1]
        os.remove(file1)
        self.assertTrue(is_valid_file(file1))

    def test_is_valid_path_on_uncreatable_file(self):
        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a file name with a char forbidden in POSIX and WIN*
            forbidden_char = "/"
            file_name = "SOMEDIR{}".format(forbidden_char)
            file_path = os.path.join(parent_directory, file_name)

            # Assert that the forbidden character prohibited path creation
            self.assertFalse(is_valid_file(file_path))


class TestFileExtension(unittest.TestCase):
    def test_get_extension_on_extension(self):
        with tempfile.NamedTemporaryFile(suffix=".EXT") as file1:
            self.assertEqual(get_extension(file1.name), "EXT")

    def test_get_extension_on_no_extension(self):
        with tempfile.NamedTemporaryFile() as file1:
            self.assertEqual(get_extension(file1.name), "")

    def test_get_extension_on_two_word_extension(self):
        with tempfile.NamedTemporaryFile(suffix=".tar.gz") as file1:
            self.assertEqual(get_extension(file1.name), "gz")
