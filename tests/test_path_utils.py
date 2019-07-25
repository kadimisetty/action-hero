import unittest
import tempfile
import shutil
import stat
import os

from action_heroes.path_utils import (
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
        with tempfile.TemporaryDirectory() as directory:
            self.assertTrue(is_existing_directory(directory))

    def test_is_existing_directory_on_nonexisting_directory(self):
        # Create and Remove a directory to confirm it doesnt exist
        nonexistent_directory = tempfile.mkdtemp()
        os.rmdir(nonexistent_directory)

        self.assertFalse(is_existing_directory(nonexistent_directory))

    def test_is_existing_file_on_exisiting_file(self):
        with tempfile.NamedTemporaryFile() as temporary_file:
            self.assertTrue(is_existing_file(temporary_file.name))

    def test_is_existing_file_on_nonexisting_file(self):
        # Create and Remove a file to confirm it doesnt exist
        nonexistent_file = tempfile.mkstemp()[1]
        os.remove(nonexistent_file)

        self.assertFalse(is_existing_file(nonexistent_file))

    def test_is_existing_path_on_exisiting_file(self):
        with tempfile.NamedTemporaryFile() as temporary_path:
            self.assertTrue(is_existing_path(temporary_path.name))

    def test_is_existing_path_on_nonexisting_file(self):
        # Create and Remove a file to confirm it doesnt exist
        nonexistent_path = tempfile.mkstemp()[1]
        os.remove(nonexistent_path)

        self.assertFalse(is_existing_path(nonexistent_path))

    def test_is_existing_path_on_exisiting_directory(self):
        with tempfile.TemporaryDirectory() as path:
            self.assertTrue(is_existing_path(path))

    def test_is_existing_path_on_nonexisting_directory(self):
        # Create and Remove a directory to confirm it doesnt exist
        nonexistent_path = tempfile.mkdtemp()
        os.rmdir(nonexistent_path)

        self.assertFalse(is_existing_path(nonexistent_path))


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
        with tempfile.TemporaryDirectory() as directory:
            self.assertTrue(is_writable_directory(directory))

    def test_is_writable_directory_on_unwritable_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            self._remove_write_permission(directory)
            self.assertFalse(is_writable_directory(directory))

    def test_is_writable_file_on_writable_file(self):
        with tempfile.NamedTemporaryFile() as temporary_file:
            self.assertTrue(is_writable_file(temporary_file.name))

    def test_is_writable_file_on_unwritable_file(self):
        with tempfile.NamedTemporaryFile() as temporary_file:
            self._remove_write_permission(temporary_file.name)
            self.assertFalse(is_writable_file(temporary_file.name))

    def test_is_writable_path_on_writable_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertTrue(is_writable_path(directory))

    def test_is_writable_path_on_unwritable_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            self._remove_write_permission(directory)
            self.assertFalse(is_writable_path(directory))

    def test_is_writable_path_on_writable_file(self):
        with tempfile.NamedTemporaryFile() as temporary_file:
            self.assertTrue(is_writable_path(temporary_file.name))

    def test_is_writable_path_on_unwritable_file(self):
        with tempfile.NamedTemporaryFile() as temporary_file:
            self._remove_write_permission(temporary_file.name)
            self.assertFalse(is_writable_path(temporary_file.name))


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
        with tempfile.TemporaryDirectory() as directory:
            self.assertTrue(is_readable_directory(directory))

    def test_is_readable_directory_on_unreadable_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            self._remove_read_permissions(directory)
            self.assertFalse(is_readable_directory(directory))

    def test_is_readable_file_on_readable_file(self):
        with tempfile.NamedTemporaryFile() as temporary_file:
            self.assertTrue(is_readable_file(temporary_file.name))

    def test_is_readable_file_on_unreadable_file(self):
        with tempfile.NamedTemporaryFile() as temporary_file:
            self._remove_read_permissions(temporary_file.name)
            self.assertFalse(is_readable_file(temporary_file.name))

    def test_is_readable_path_on_readable_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertTrue(is_readable_path(directory))

    def test_is_readable_path_on_unreadable_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            self._remove_read_permissions(directory)
            self.assertFalse(is_readable_path(directory))

    def test_is_readable_path_on_readable_file(self):
        with tempfile.NamedTemporaryFile() as temporary_file:
            self.assertTrue(is_readable_path(temporary_file.name))

    def test_is_readable_path_on_unreadable_file(self):
        with tempfile.NamedTemporaryFile() as temporary_file:
            self._remove_read_permissions(temporary_file.name)
            self.assertFalse(is_readable_path(temporary_file.name))


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
        with tempfile.TemporaryDirectory() as directory:
            self.assertTrue(is_executable_directory(directory))

    def test_is_executable_directory_on_unexecutable_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            self._remove_execute_permissions(directory)
            self.assertFalse(is_executable_directory(directory))

    def test_is_executable_file_on_executable_file(self):
        with tempfile.NamedTemporaryFile() as temporary_file:
            self._add_execute_permissions(temporary_file.name)
            self.assertTrue(is_executable_file(temporary_file.name))

    def test_is_executable_file_on_unexecutable_file(self):
        with tempfile.NamedTemporaryFile() as temporary_file:
            self._remove_execute_permissions(temporary_file.name)
            self.assertFalse(is_executable_file(temporary_file.name))

    def test_is_executable_path_on_executable_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertTrue(is_executable_path(directory))

    def test_is_executable_path_on_unexecutable_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            self._remove_execute_permissions(directory)
            self.assertFalse(is_executable_path(directory))

    def test_is_executable_path_on_executable_file(self):
        with tempfile.NamedTemporaryFile() as temporary_file:
            self._add_execute_permissions(temporary_file.name)
            self.assertTrue(is_executable_path(temporary_file.name))

    def test_is_executable_path_on_unexecutable_file(self):
        with tempfile.NamedTemporaryFile() as temporary_file:
            self.assertFalse(is_executable_path(temporary_file.name))


class TestSymbolicLinkUtils(unittest.TestCase):
    def setUp(self):
        # Create parent directory to hold symbolic links
        self.parent_directory = tempfile.mkdtemp()

        # Create temporary directory and a symbolic link pointing to it
        self.tmp_directory = tempfile.mkdtemp()
        self.link_to_tmp_directory = os.path.join(
            self.parent_directory, os.path.basename(self.tmp_directory)
        )
        os.symlink(
            src=self.tmp_directory,
            dst=self.link_to_tmp_directory,
            target_is_directory=True,
        )

        # Create temporary file and a symbolic link pointing to it
        self.tmp_file = tempfile.mkstemp()[1]
        self.link_to_tmp_file = os.path.join(
            self.parent_directory, os.path.basename(self.tmp_file)
        )
        os.symlink(src=self.tmp_file, dst=self.link_to_tmp_file)

    def tearDown(self):
        # Unlink symbolic links
        os.unlink(self.link_to_tmp_file)
        os.unlink(self.link_to_tmp_directory)

        # Remove temporary directories and file
        shutil.rmtree(self.parent_directory)
        os.rmdir(self.tmp_directory)
        os.remove(self.tmp_file)

    def test_is_symbolic_link_on_existing_link_to_directory(self):
        self.assertTrue(is_symbolic_link(self.link_to_tmp_directory))

    def test_is_symbolic_link_on_existing_link_to_file(self):
        self.assertTrue(is_symbolic_link(self.link_to_tmp_file))

    def test_is_symbolic_link_on_existing_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertFalse(is_symbolic_link(directory))

    def test_is_symbolic_link_on_existing_file(self):
        with tempfile.NamedTemporaryFile() as temporary_file:
            self.assertFalse(is_symbolic_link(temporary_file.name))


class TestResolvePath(unittest.TestCase):
    def test_resolve_path_resolves_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            expected = os.path.realpath(directory)
            self.assertEqual(resolve_path(directory), expected)

    def test_resolve_path_resolves_file(self):
        with tempfile.NamedTemporaryFile() as temporary_file:
            expected = os.path.realpath(temporary_file.name)
            self.assertEqual(resolve_path(temporary_file.name), expected)


class TestCreatePath(unittest.TestCase):
    def test_create_directory(self):
        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a directory in termporary directory
            filename = os.path.join(parent_directory, "SOMEDIR")
            create_directory(filename)

            # Check if directory was created successfully
            self.assertTrue(os.path.isdir(filename), True)

    def test_create_file(self):
        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a file in termporary directory
            filename = os.path.join(parent_directory, "SOMEFILE")
            create_file(filename)

            # Check if file was created successfully
            self.assertTrue(os.path.isfile(filename), True)


class TestExistingOrCreatablePath(unittest.TestCase):
    def test_is_existing_or_creatable_path_on_existing_dir(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertTrue(is_existing_or_creatable_path(directory))

    def test_is_existing_or_creatable_path_on_nonexisting_creatable_dir(self):
        # Create and delete a temp directory so we know that it is a valid path
        directory = tempfile.mkdtemp()
        os.rmdir(directory)
        self.assertTrue(is_existing_or_creatable_path(directory))

    def test_is_existing_or_creatable_path_on_uncreatable_dir(self):
        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a directory name with a char forbidden in POSIX and WIN*
            forbidden_char = "/"
            directory_name = "SOMEDIR{}".format(forbidden_char)
            directory_path = os.path.join(parent_directory, directory_name)

            # Assert that the forbidden character prohibited path creation
            self.assertFalse(is_existing_or_creatable_path(directory_path))

    def test_is_existing_or_creatable_path_on_existing_file(self):
        with tempfile.NamedTemporaryFile() as temporary_file:
            self.assertTrue(is_existing_or_creatable_path(temporary_file.name))

    def test_is_existing_or_creatable_path_on_nonexisting_creatable_file(self):
        # Create and delete a temp file so we know that it is a valid path
        temporary_file = tempfile.mkstemp()[1]
        os.remove(temporary_file)
        self.assertTrue(is_existing_or_creatable_path(temporary_file))

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
        with tempfile.TemporaryDirectory() as directory:
            self.assertTrue(is_valid_path(directory))

    def test_is_valid_path_on_nonexisting_creatable_dir(self):
        # Create and delete a temp directory so we know that it is a valid path
        directory = tempfile.mkdtemp()
        os.rmdir(directory)
        self.assertTrue(is_valid_path(directory))

    def test_is_valid_path_on_uncreatable_dir(self):
        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a directory name with a char forbidden in POSIX and WIN*
            forbidden_char = "/"
            directory_name = "SOMEDIR{}".format(forbidden_char)
            directory_path = os.path.join(parent_directory, directory_name)

            # Assert that the forbidden character prohibited path creation
            self.assertFalse(is_valid_path(directory_path))

    def test_is_valid_path_on_existing_file(self):
        with tempfile.NamedTemporaryFile() as temporary_file:
            self.assertTrue(is_valid_path(temporary_file.name))

    def test_is_valid_path_on_nonexisting_creatable_file(self):
        # Create and delete a temp file so we know that it is a valid path
        temporary_file = tempfile.mkstemp()[1]
        os.remove(temporary_file)
        self.assertTrue(is_valid_path(temporary_file))

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
        with tempfile.TemporaryDirectory() as directory:
            self.assertTrue(is_valid_directory(directory))

    def test_is_valid_path_on_nonexisting_creatable_dir(self):
        # Create and delete a temp directory so we know that it is a valid path
        directory = tempfile.mkdtemp()
        os.rmdir(directory)
        self.assertTrue(is_valid_directory(directory))

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
        with tempfile.NamedTemporaryFile() as temporary_file:
            self.assertTrue(is_valid_file(temporary_file.name))

    def test_is_valid_path_on_nonexisting_creatable_file(self):
        # Create and delete a temp file so we know that it is a valid path
        temporary_file = tempfile.mkstemp()[1]
        os.remove(temporary_file)
        self.assertTrue(is_valid_file(temporary_file))

    def test_is_valid_path_on_uncreatable_file(self):
        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a file name with a char forbidden in POSIX and WIN*
            forbidden_char = "/"
            file_name = "SOMEDIR{}".format(forbidden_char)
            file_path = os.path.join(parent_directory, file_name)

            # Assert that the forbidden character prohibited path creation
            self.assertFalse(is_valid_file(file_path))
