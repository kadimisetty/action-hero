import os


__all__ = [
    "is_executable_directory",
    "is_executable_file",
    "is_executable_path",
    "is_existing_directory",
    "is_existing_file",
    "is_existing_path",
    "is_readable_directory",
    "is_readable_file",
    "is_readable_path",
    "is_symbolic_link",
    "is_writable_directory",
    "is_writable_file",
    "is_writable_path"
]


def is_symbolic_link(path):
    """Return True if path is existing directory that is a symbolic link"""
    return os.path.islink(path)


def is_existing_directory(path):
    """Returns True if path is an existing directory"""
    return os.path.isdir(path)


def is_readable_directory(path):
    """Returns True if path is a directory with read permissible flag set"""
    return is_readable_path(path)


def is_writable_directory(path):
    """Returns True if path is a directory with write permissible flag set"""
    return is_writable_path(path)


def is_executable_directory(path):
    """Returns True if path is a directory with execute permissible flag set"""
    return is_executable_path(path)


def is_existing_file(path):
    """Returns True if path is an existing file"""
    return os.path.isfile(path)


def is_readable_file(path):
    """Returns True if path is a file with read permissible flag set"""
    return is_readable_path(path)


def is_writable_file(path):
    """Returns True if path is a file with write permissible flag set"""
    return is_writable_path(path)


def is_executable_file(path):
    """Return True if path is a file with execute permissible flag set"""
    return is_executable_path(path)


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
