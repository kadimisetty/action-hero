import os
import pathlib


__all__ = [
    "create_directory",
    "create_file",
    "get_extension",
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
    "resolve_path",
]


def get_extension(path):
    """Fet file extension/prefix"""
    suffix = pathlib.Path(path).suffix
    # Return suffix is nonempty without the starting dot
    # or blank string if theres none
    if suffix and suffix.startswith("."):
        return suffix[1:]
    else:
        return ""


def create_file(path):
    """Creates a file with name of path"""
    pathlib.Path(path).touch()


def create_directory(path):
    """Creates a directory with name of path"""
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


def is_existing_or_creatable_path(path):
    """Returns True if path already exists or is creatable by current User

    IMPORTANT NOTE:
        This solution is a work-around, in that, an ignorable tempfile with a
        shortlife is created and removed.
        Source: https://stackoverflow.com/a/48499049/225903

        For a better, although far more complicated solution, read:
        https://stackoverflow.com/a/34102855/225903

    """
    try:
        # Mode x: Open for exclusive creation, fail if the path already exists
        with open(path, mode='x') as _:
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
    """
    Returns True if directoy as path already exists or is creatable by current
    User

    """
    return is_valid_path(path)


def is_valid_file(path):
    """
    Returns True if file as path already exists or is creatable by current
    User

    """
    return is_valid_path(path)
