import unittest
import tempfile
import shutil
import os

from action_hero.path_utils import (
    add_execute_permission,
    create_directory,
    create_file,
    get_extension,
    is_empty_file,
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
    remove_execute_permission,
    remove_read_permission,
    remove_write_permission,
    resolve_path,
)


class TestExistenceUtils(unittest.TestCase):
    def test_on_exisiting_directory(self):
        """
        Test if a temporary directory exists.

        Args:
            self: (todo): write your description
        """
        with tempfile.TemporaryDirectory() as dir1:
            self.assertTrue(is_existing_directory(dir1))

    def test_on_nonexisting_directory(self):
        """
        Create a temporary directory.

        Args:
            self: (todo): write your description
        """
        dir1 = tempfile.mkdtemp()
        os.rmdir(dir1)

        self.assertFalse(is_existing_directory(dir1))

    def test_on_exisiting_file(self):
        """
        Test if a testfile exists.

        Args:
            self: (todo): write your description
        """
        with tempfile.NamedTemporaryFile() as file1:
            self.assertTrue(is_existing_file(file1.name))

    def test_on_nonexisting_file(self):
        """
        Test if the file exists.

        Args:
            self: (todo): write your description
        """
        # Create and Remove a file to confirm it doesnt exist
        file1 = tempfile.mkstemp()[1]
        os.remove(file1)

        self.assertFalse(is_existing_file(file1))

    def test_on_exisiting_path_as_file(self):
        """
        Sets the test file1 : path : path2.

        Args:
            self: (todo): write your description
        """
        with tempfile.NamedTemporaryFile() as file1:
            self.assertTrue(is_existing_path(file1.name))

    def test_on_nonexisting_path_as_file(self):
        """
        Test if a temp file exists.

        Args:
            self: (todo): write your description
        """
        # Create and Remove a file to confirm it doesnt exist
        file1 = tempfile.mkstemp()[1]
        os.remove(file1)

        self.assertFalse(is_existing_path(file1))

    def test_on_exisiting_path_as_directory(self):
        """
        Test if the given path exists.

        Args:
            self: (todo): write your description
        """
        with tempfile.TemporaryDirectory() as dir1:
            self.assertTrue(is_existing_path(dir1))

    def test_on_nonexisting_path_as_directory(self):
        """
        Test if the temporary directory exists.

        Args:
            self: (todo): write your description
        """
        # Create and Remove a directory to confirm it doesnt exist
        dir1 = tempfile.mkdtemp()
        os.rmdir(dir1)

        self.assertFalse(is_existing_path(dir1))


class TestWritableUtils(unittest.TestCase):
    def test_on_writable_directory(self):
        """
        Test if the directory.

        Args:
            self: (todo): write your description
        """
        with tempfile.TemporaryDirectory() as dir1:
            self.assertTrue(is_writable_directory(dir1))

    def test_on_unwritable_directory(self):
        """
        Test if the given directory exists.

        Args:
            self: (todo): write your description
        """
        with tempfile.TemporaryDirectory() as dir1:
            remove_write_permission(dir1)
            self.assertFalse(is_writable_directory(dir1))

    def test_on_writable_file(self):
        """
        Test if the file is writable.

        Args:
            self: (todo): write your description
        """
        with tempfile.NamedTemporaryFile() as file1:
            self.assertTrue(is_writable_file(file1.name))

    def test_on_unwritable_file(self):
        """
        Test if the file is writable.

        Args:
            self: (todo): write your description
        """
        with tempfile.NamedTemporaryFile() as file1:
            remove_write_permission(file1.name)
            self.assertFalse(is_writable_file(file1.name))

    def test_on_writable_pasth_as_directory(self):
        """
        Test if a temporary directory is writable.

        Args:
            self: (todo): write your description
        """
        with tempfile.TemporaryDirectory() as dir1:
            self.assertTrue(is_writable_path(dir1))

    def test_on_unwritable_path_as_directory(self):
        """
        Test if the given path is writable.

        Args:
            self: (todo): write your description
        """
        with tempfile.TemporaryDirectory() as dir1:
            remove_write_permission(dir1)
            self.assertFalse(is_writable_path(dir1))

    def test_on_writable_path_as_file(self):
        """
        Test if a temporary file exists. writeable.

        Args:
            self: (todo): write your description
        """
        with tempfile.NamedTemporaryFile() as file1:
            self.assertTrue(is_writable_path(file1.name))

    def test_on_unwritable_path_as_file(self):
        """
        Test if the given file is writable.

        Args:
            self: (todo): write your description
        """
        with tempfile.NamedTemporaryFile() as file1:
            remove_write_permission(file1.name)
            self.assertFalse(is_writable_path(file1.name))


class TestReadableUtils(unittest.TestCase):
    def test_on_readable_directory(self):
        """
        Test if a temporary directory.

        Args:
            self: (todo): write your description
        """
        # Specify temporary directory
        with tempfile.TemporaryDirectory() as dir1:
            self.assertTrue(is_readable_directory(dir1))

    def test_on_unreadable_directory(self):
        """
        Test if a temporary directory.

        Args:
            self: (todo): write your description
        """
        dir1 = tempfile.mkdtemp()
        remove_read_permission(dir1)
        self.assertFalse(is_readable_directory(dir1))
        os.rmdir(dir1)

    def test_on_readable_file(self):
        """
        : return : : class : attr : tempfile.

        Args:
            self: (todo): write your description
        """
        with tempfile.NamedTemporaryFile() as file1:
            self.assertTrue(is_readable_file(file1.name))

    def test_on_unreadable_file(self):
        """
        Test if the file is unreadable.

        Args:
            self: (todo): write your description
        """
        with tempfile.NamedTemporaryFile() as file1:
            remove_read_permission(file1.name)
            self.assertFalse(is_readable_file(file1.name))

    def test_on_readable_path_as_directory(self):
        """
        Test if the given path exists.

        Args:
            self: (todo): write your description
        """
        with tempfile.TemporaryDirectory() as dir1:
            self.assertTrue(is_readable_path(dir1))

    def test_on_unreadable_path_as_directory(self):
        """
        Test if the given directory exists.

        Args:
            self: (todo): write your description
        """
        dir1 = tempfile.mkdtemp()
        remove_read_permission(dir1)
        self.assertFalse(is_readable_directory(dir1))
        os.rmdir(dir1)

    def test_on_readable_path_as_file(self):
        """
        Test if a temp file exists.

        Args:
            self: (todo): write your description
        """
        with tempfile.NamedTemporaryFile() as file1:
            self.assertTrue(is_readable_path(file1.name))

    def test_on_unreadable_path_as_file(self):
        """
        Test if the given path is unreadable.

        Args:
            self: (todo): write your description
        """
        with tempfile.NamedTemporaryFile() as file1:
            remove_read_permission(file1.name)
            self.assertFalse(is_readable_path(file1.name))


class TestExecutableUtils(unittest.TestCase):
    def test_on_executable_directory(self):
        """
        Create a temporary directory. executable.

        Args:
            self: (todo): write your description
        """
        with tempfile.TemporaryDirectory() as dir1:
            self.assertTrue(is_executable_directory(dir1))

    def test_on_unexecutable_directory(self):
        """
        Removes the given directory.

        Args:
            self: (todo): write your description
        """
        with tempfile.TemporaryDirectory() as dir1:
            remove_execute_permission(dir1)
            self.assertFalse(is_executable_directory(dir1))

    def test_on_executable_file(self):
        """
        Test if file on - like a file.

        Args:
            self: (todo): write your description
        """
        with tempfile.NamedTemporaryFile() as file1:
            add_execute_permission(file1.name)
            self.assertTrue(is_executable_file(file1.name))

    def test_on_unexecutable_file(self):
        """
        Test if the given file1 and run it on the executable.

        Args:
            self: (todo): write your description
        """
        with tempfile.NamedTemporaryFile() as file1:
            remove_execute_permission(file1.name)
            self.assertFalse(is_executable_file(file1.name))

    def test_on_executable_path_as_directory(self):
        """
        Test if the given directory.

        Args:
            self: (todo): write your description
        """
        with tempfile.TemporaryDirectory() as dir1:
            self.assertTrue(is_executable_path(dir1))

    def test_on_unexecutable_path_as_directory(self):
        """
        Test if the given executable is unexecutable.

        Args:
            self: (todo): write your description
        """
        with tempfile.TemporaryDirectory() as dir1:
            remove_execute_permission(dir1)
            self.assertFalse(is_executable_path(dir1))

    def test_on_executable_path_as_file(self):
        """
        Test if the given path : path2. path to the executable file.

        Args:
            self: (todo): write your description
        """
        with tempfile.NamedTemporaryFile() as file1:
            add_execute_permission(file1.name)
            self.assertTrue(is_executable_path(file1.name))

    def test_on_unexecutable_path_as_file(self):
        """
        Test if the executable on a file exists.

        Args:
            self: (todo): write your description
        """
        with tempfile.NamedTemporaryFile() as file1:
            self.assertFalse(is_executable_path(file1.name))


class TestSymbolicLinkUtils(unittest.TestCase):
    def setUp(self):
        """
        Create a symbolic link.

        Args:
            self: (todo): write your description
        """
        # Create parent directory to hold symbolic links
        self.parent_directory = tempfile.mkdtemp()

        # Create temporary directory and a symbolic link pointing to it
        self.dir1 = tempfile.mkdtemp()
        self.link_to_dir1 = os.path.join(
            self.parent_directory, os.path.basename(self.dir1)
        )
        os.symlink(
            src=self.dir1, dst=self.link_to_dir1, target_is_directory=True
        )

        # Create temporary file and a symbolic link pointing to it
        self.file1 = tempfile.mkstemp()[1]
        self.link_to_file1 = os.path.join(
            self.parent_directory, os.path.basename(self.file1)
        )
        os.symlink(src=self.file1, dst=self.link_to_file1)

    def tearDown(self):
        """
        Tear down link.

        Args:
            self: (todo): write your description
        """
        # Unlink symbolic links
        os.unlink(self.link_to_file1)
        os.unlink(self.link_to_dir1)

        # Remove temporary directories and file
        shutil.rmtree(self.parent_directory)
        os.rmdir(self.dir1)
        os.remove(self.file1)

    def test_on_existing_link_to_directory(self):
        """
        Test if the given link_on_to_directory.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(is_symbolic_link(self.link_to_dir1))

    def test_on_existing_link_to_file(self):
        """
        Test if a symbolic link is not already existing.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(is_symbolic_link(self.link_to_file1))

    def test_on_existing_directory(self):
        """
        Create a temporary directory.

        Args:
            self: (todo): write your description
        """
        with tempfile.TemporaryDirectory() as temporary_directory:
            self.assertFalse(is_symbolic_link(temporary_directory))

    def test_on_existing_file(self):
        """
        Create a temporary file on a temporary file.

        Args:
            self: (todo): write your description
        """
        with tempfile.NamedTemporaryFile() as temporary_file:
            self.assertFalse(is_symbolic_link(temporary_file.name))


class TestResolvePath(unittest.TestCase):
    def test_on_directory(self):
        """
        Create a temporary directory.

        Args:
            self: (todo): write your description
        """
        with tempfile.TemporaryDirectory() as dir1:
            expected = os.path.realpath(dir1)
            self.assertEqual(resolve_path(dir1), expected)

    def test_on_file(self):
        """
        Test if a test file.

        Args:
            self: (todo): write your description
        """
        with tempfile.NamedTemporaryFile() as file1:
            expected = os.path.realpath(file1.name)
            self.assertEqual(resolve_path(file1.name), expected)


class TestCreatePath(unittest.TestCase):
    def test_create_directory(self):
        """
        Create a new directory.

        Args:
            self: (todo): write your description
        """
        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a directory in termporary directory
            dir1 = os.path.join(parent_directory, "SOMEDIR")
            create_directory(dir1)

            # Check if directory was created successfully
            self.assertTrue(os.path.isdir(dir1), True)

    def test_create_file(self):
        """
        Create a new file.

        Args:
            self: (todo): write your description
        """
        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a file in termporary directory
            file1 = os.path.join(parent_directory, "SOMEFILE")
            create_file(file1)

            # Check if file was created successfully
            self.assertTrue(os.path.isfile(file1), True)


class TestExistingOrCreatablePath(unittest.TestCase):
    def test_on_existing_dir(self):
        """
        Test if a temporary directory exists.

        Args:
            self: (todo): write your description
        """
        with tempfile.TemporaryDirectory() as dir1:
            self.assertTrue(is_existing_or_creatable_path(dir1))

    def test_on_nonexisting_creatable_dir(self):
        """
        Test if the temporary dir exists.

        Args:
            self: (todo): write your description
        """
        # Create and delete a temp directory so we know that it is a valid path
        dir1 = tempfile.mkdtemp()
        os.rmdir(dir1)
        self.assertTrue(is_existing_or_creatable_path(dir1))

    def test_on_uncreatable_dir(self):
        """
        Test if the given directory exists.

        Args:
            self: (todo): write your description
        """
        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a directory name with a char forbidden in POSIX and WIN*
            forbidden_char = "/"
            directory_name = "SOMEDIR{}".format(forbidden_char)
            directory_path = os.path.join(parent_directory, directory_name)

            # Assert that the forbidden character prohibited path creation
            self.assertFalse(is_existing_or_creatable_path(directory_path))

    def test_on_existing_file(self):
        """
        Test if a file exists.

        Args:
            self: (todo): write your description
        """
        with tempfile.NamedTemporaryFile() as file1:
            self.assertTrue(is_existing_or_creatable_path(file1.name))

    def test_on_nonexisting_creatable_file(self):
        """
        Test if a temporary file exists.

        Args:
            self: (todo): write your description
        """
        # Create and delete a temp file so we know that it is a valid path
        file1 = tempfile.mkstemp()[1]
        os.remove(file1)
        self.assertTrue(is_existing_or_creatable_path(file1))

    def test_on_uncreatable_file(self):
        """
        Test if a tempfile is a new directory.

        Args:
            self: (todo): write your description
        """
        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a file name with a char forbidden in POSIX and WIN*
            forbidden_char = "/"
            file_name = "SOMEDIR{}".format(forbidden_char)
            file_path = os.path.join(parent_directory, file_name)

            # Assert that the forbidden character prohibited path creation
            self.assertFalse(is_existing_or_creatable_path(file_path))


class TestValidPath(unittest.TestCase):
    def test_on_existing_dir(self):
        """
        Create a temporary directory exists.

        Args:
            self: (todo): write your description
        """
        with tempfile.TemporaryDirectory() as dir1:
            self.assertTrue(is_valid_path(dir1))

    def test_on_nonexisting_creatable_dir(self):
        """
        Ensure that the temp file exists. temporary.

        Args:
            self: (todo): write your description
        """
        # Create and delete a temp directory so we know that it is a valid path
        dir1 = tempfile.mkdtemp()
        os.rmdir(dir1)
        self.assertTrue(is_valid_path(dir1))

    def test_on_uncreatable_dir(self):
        """
        Test if the given directories existreatable directory.

        Args:
            self: (todo): write your description
        """
        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a directory name with a char forbidden in POSIX and WIN*
            forbidden_char = "/"
            directory_name = "SOMEDIR{}".format(forbidden_char)
            directory_path = os.path.join(parent_directory, directory_name)

            # Assert that the forbidden character prohibited path creation
            self.assertFalse(is_valid_path(directory_path))

    def test_on_existing_file(self):
        """
        Test if a file exists.

        Args:
            self: (todo): write your description
        """
        with tempfile.NamedTemporaryFile() as file1:
            self.assertTrue(is_valid_path(file1.name))

    def test_on_nonexisting_creatable_file(self):
        """
        Ensures that file exists.

        Args:
            self: (todo): write your description
        """
        # Create and delete a temp file so we know that it is a valid path
        file1 = tempfile.mkstemp()[1]
        os.remove(file1)
        self.assertTrue(is_valid_path(file1))

    def test_on_uncreatable_file(self):
        """
        Test if the test files in - directories exist.

        Args:
            self: (todo): write your description
        """
        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a file name with a char forbidden in POSIX and WIN*
            forbidden_char = "/"
            file_name = "SOMEDIR{}".format(forbidden_char)
            file_path = os.path.join(parent_directory, file_name)

            # Assert that the forbidden character prohibited path creation
            self.assertFalse(is_valid_path(file_path))


class TestValidDirectory(unittest.TestCase):
    def test_on_existing_dir(self):
        """
        Create a temporary directory exists.

        Args:
            self: (todo): write your description
        """
        with tempfile.TemporaryDirectory() as dir1:
            self.assertTrue(is_valid_directory(dir1))

    def test_on_nonexisting_creatable_dir(self):
        """
        Test if the tempfile exists.

        Args:
            self: (todo): write your description
        """
        # Create and delete a temp directory so we know that it is a valid path
        dir1 = tempfile.mkdtemp()
        os.rmdir(dir1)
        self.assertTrue(is_valid_directory(dir1))

    def test_on_uncreatable_dir(self):
        """
        Ensure that all the directories existreatable.

        Args:
            self: (todo): write your description
        """
        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a directory name with a char forbidden in POSIX and WIN*
            forbidden_char = "/"
            directory_name = "SOMEDIR{}".format(forbidden_char)
            directory_path = os.path.join(parent_directory, directory_name)

            # Assert that the forbidden character prohibited path creation
            self.assertFalse(is_valid_directory(directory_path))


class TestValidFile(unittest.TestCase):
    def test_on_existing_file(self):
        """
        Test if a file exists.

        Args:
            self: (todo): write your description
        """
        with tempfile.NamedTemporaryFile() as file1:
            self.assertTrue(is_valid_file(file1.name))

    def test_on_nonexisting_creatable_file(self):
        """
        Test if a file is none exists.

        Args:
            self: (todo): write your description
        """
        # Create and delete a temp file so we know that it is a valid path
        file1 = tempfile.mkstemp()[1]
        os.remove(file1)
        self.assertTrue(is_valid_file(file1))

    def test_on_uncreatable_file(self):
        """
        Ensure that the test files exist.

        Args:
            self: (todo): write your description
        """
        with tempfile.TemporaryDirectory() as parent_directory:
            # Create a file name with a char forbidden in POSIX and WIN*
            forbidden_char = "/"
            file_name = "SOMEDIR{}".format(forbidden_char)
            file_path = os.path.join(parent_directory, file_name)

            # Assert that the forbidden character prohibited path creation
            self.assertFalse(is_valid_file(file_path))


class TestFileExtension(unittest.TestCase):
    def test_on_extension(self):
        """
        Test if the file extension has the file extension.

        Args:
            self: (todo): write your description
        """
        with tempfile.NamedTemporaryFile(suffix=".EXT") as file1:
            self.assertEqual(get_extension(file1.name), "EXT")

    def test_on_no_extension(self):
        """
        Create a temporary file exists.

        Args:
            self: (todo): write your description
        """
        with tempfile.NamedTemporaryFile() as file1:
            self.assertEqual(get_extension(file1.name), "")

    def test_on_two_word_extension(self):
        """
        Test if two two - word word exist.

        Args:
            self: (todo): write your description
        """
        with tempfile.NamedTemporaryFile(suffix=".tar.gz") as file1:
            self.assertEqual(get_extension(file1.name), "gz")


class TestFileIsEmpty(unittest.TestCase):
    def test_on_empty_file(self):
        """
        Test if the file is empty.

        Args:
            self: (todo): write your description
        """
        with tempfile.NamedTemporaryFile() as file1:
            self.assertTrue(is_empty_file(file1.name))

    def test_on_nonempty_file(self):
        """
        Test to a nonempty on disk.

        Args:
            self: (todo): write your description
        """
        with tempfile.NamedTemporaryFile() as file1:
            with open(file1.name, "a") as file_for_writing:
                file_for_writing.write("SOME TEXT")
            self.assertFalse(is_empty_file(file1.name))
