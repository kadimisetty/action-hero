import os
import stat
import pathlib


__all__ = [
    "add_execute_permission",
    "create_directory",
    "create_file",
    "get_extension",
    "is_empty_file",
    "is_executable_directory",
    "is_executable_file",
    "is_executable_path",
    "is_existing_directory",
    "is_existing_file",
    "is_existing_or_creatable_path",
    "is_existing_path",
    "is_readable_directory",
    "is_readable_file",
    "is_readable_path",
    "is_symbolic_link",
    "is_valid_directory",
    "is_valid_file",
    "is_valid_path",
    "is_writable_directory",
    "is_writable_file",
    "is_writable_path",
    "remove_execute_permission",
    "remove_read_permission",
    "remove_write_permission",
    "resolve_path",
]


def get_extension(path):
    """Get file extension/prefix

    The dot is strippped if there is one.

    Args:
        path (str): Filename

    Returns:
        (str) File extension or blank string

    """
    suffix = pathlib.Path(path).suffix
    # Return suffix is nonempty without the starting dot
    # or blank string if theres none
    if suffix and suffix.startswith("."):
        return suffix[1:]
    else:
        return ""


def create_file(path):
    """Creates a file with name of path

    When exist_ok=True is set to True on touch(), the file's modification date
    will be set yet a new file is not created over it. Else, when a file
    already exists there, it might raise a FileExistsError. TODO: Visit this
    behavior again.

    Args:
        path (str): Path to create file
    """
    pathlib.Path(path).touch(exist_ok=True)


def create_directory(path):
    """Creates a directory with name of path

    Args:
        path (str): Path to create directory

    Raises:
        FileExistsError: Raised if path is already present
    """
    os.mkdir(path)


def is_symbolic_link(path):
    """Return True if path is existing directory that is a symbolic link"""
    return os.path.islink(path)


def is_existing_directory(path):
    """Returns True if path is an existing directory"""
    return os.path.isdir(path)


def is_readable_directory(path):
    """Returns True if path is a directory with read permissible flag set"""
    return is_existing_directory(path) and is_readable_path(path)


def is_writable_directory(path):
    """Returns True if path is a directory with write permissible flag set"""
    return is_existing_directory(path) and is_writable_path(path)


def is_executable_directory(path):
    """Returns True if path is a directory with execute permissible flag set"""
    return is_existing_directory(path) and is_executable_path(path)


def is_existing_file(path):
    """Returns True if path is an existing file"""
    return os.path.isfile(path)


def is_readable_file(path):
    """Returns True if path is a file with read permissible flag set"""
    return is_existing_file(path) and is_readable_path(path)


def is_writable_file(path):
    """Returns True if path is a file with write permissible flag set"""
    return is_existing_file(path) and is_writable_path(path)


def is_executable_file(path):
    """Return True if path is a file with execute permissible flag set"""
    return is_existing_file(path) and is_executable_path(path)


def is_existing_path(path):
    """Returns True if path exists"""
    return os.path.exists(path)


def is_writable_path(path):
    """Returns True if path has write permissible flag set"""
    return os.access(path, os.W_OK)


def is_readable_path(path):
    """Returns True if path has read permission flag set"""
    return os.access(path, os.R_OK)


def is_executable_path(path):
    """Returns True if path has execute permission flag set"""
    return os.access(path, os.X_OK)


def resolve_path(path):
    """Returns resolved canonical path removing symbolic links if present"""
    return os.path.realpath(path)
    # return str(pathlib.Path(path).resolve())


def is_existing_or_creatable_path(path):
    """Returns True if path already exists or is creatable by current User

    This solution is a work-around, in that, an ignorable tempfile with a
    shortlife is created and removed.
    Source: https://stackoverflow.com/a/48499049/225903

    For a better, although far more complicated solution, read:
    https://stackoverflow.com/a/34102855/225903

    Args:
        path (str): Path to check for existence or creatability

    """
    try:
        # Mode x: Open for exclusive creation, fail if the path already exists
        with open(path, mode="x") as _:
            # Raises OSError if:
            # Condition 1. file exists
            # Condition 2. Unable to create at path

            # Else successfully able to create at path
            return True

    except OSError:
        # Handle Condition 1. Path exists
        if os.path.isfile(path) or os.path.isdir(path):
            return True
        # Handle Condition 2. Unable to create at path
        return False


def is_valid_path(path):
    """Returns True if path already exists or is creatable by current User"""
    return is_existing_or_creatable_path(path)


def is_valid_directory(path):
    """ Returns True if directoy as path already exists or is creatable by
    current User.

    """
    return is_valid_path(path)


def is_valid_file(path):
    """Returns True if file as path already exists or is creatable by current
    User

    """
    return is_valid_path(path)


def remove_write_permission(path):
    """Remove write permissions and keep other permissions intact.

    Source:
        https://stackoverflow.com/a/38511116/225903

    Args:
        path (str):  The path whose permissions to alter.

    """
    NO_USER_WRITING = ~stat.S_IWUSR
    NO_GROUP_WRITING = ~stat.S_IWGRP
    NO_OTHER_WRITING = ~stat.S_IWOTH
    NO_WRITING = NO_USER_WRITING & NO_GROUP_WRITING & NO_OTHER_WRITING

    current_permissions = stat.S_IMODE(os.lstat(path).st_mode)
    os.chmod(path, current_permissions & NO_WRITING)


def remove_read_permission(path):
    """Remove read permissions and keep other permissions intact.

    Source:
        https://stackoverflow.com/a/38511116/225903

    Args:
        path (str):  The path whose permissions to alter.
    """
    NO_USER_READING = ~stat.S_IRUSR
    NO_GROUP_READING = ~stat.S_IRGRP
    NO_OTHER_READING = ~stat.S_IROTH
    NO_READING = NO_USER_READING & NO_GROUP_READING & NO_OTHER_READING

    current_permissions = stat.S_IMODE(os.lstat(path).st_mode)
    os.chmod(path, current_permissions & NO_READING)


def remove_execute_permission(path):
    """Remove execute permissions and keep other permissions intact.

    Source:
        https://stackoverflow.com/a/38511116/225903

    Args:
        path (str):  The path whose permissions to alter.

    """
    NO_USER_EXECUTING = ~stat.S_IXUSR
    NO_GROUP_EXECUTING = ~stat.S_IXGRP
    NO_OTHER_EXECUTING = ~stat.S_IXOTH
    NO_EXECUTING = (
        NO_USER_EXECUTING & NO_GROUP_EXECUTING & NO_OTHER_EXECUTING
    )

    current_permissions = stat.S_IMODE(os.lstat(path).st_mode)
    os.chmod(path, current_permissions & NO_EXECUTING)


def add_execute_permission(path):
    """Add execute permission and keep other permissions intact.

    Source:
        https://stackoverflow.com/a/38511116/225903

    Args:
        path:  The path whose permissions to alter.

    """
    USER_EXECUTING = stat.S_IXUSR
    GROUP_EXECUTING = stat.S_IXGRP
    OTHER_EXECUTING = stat.S_IXOTH
    EXECUTING = USER_EXECUTING | GROUP_EXECUTING | OTHER_EXECUTING

    current_permissions = stat.S_IMODE(os.lstat(path).st_mode)
    os.chmod(path, current_permissions | EXECUTING)


def is_empty_file(path):
    """Returns True if file is empty"""
    return is_existing_file(path) and os.stat(path).st_size == 0
