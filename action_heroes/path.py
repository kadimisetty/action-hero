from argparse import Action

from action_heroes.path_utils import (
    create_directory,
    create_file,
    is_existing_directory,
    is_existing_file,
    is_existing_path,
    is_readable_directory,
    is_readable_file,
    is_readable_path,
    is_valid_directory,
    is_valid_file,
    is_valid_path,
    is_writable_directory,
    is_writable_file,
    is_writable_path,
    resolve_path,
)


__all__ = [
    "DirectoryDoesNotExistAction",
    "DirectoryExistsAction",
    "DirectoryIsExecutableAction",
    "DirectoryIsNotExecutableAction",
    "DirectoryIsNotReadableAction",
    "DirectoryIsNotWritableAction",
    "DirectoryIsReadableAction",
    "DirectoryIsValidAction",
    "DirectoryIsWritableAction",
    "EnsureDirectoryAction",
    "EnsureFileAction",
    "FileDoesNotExistAction",
    "FileExistsAction",
    "FileHasExtension",
    "FileIsEmptyAction",
    "FileIsExecutableAction",
    "FileIsNotEmptyAction",
    "FileIsNotExecutableAction",
    "FileIsNotReadableAction",
    "FileIsNotWritableAction",
    "FileIsReadableAction",
    "FileIsValidAction",
    "FileIsWritableAction",
    "PathDoesNotExistsAction",
    "PathExistsAction",
    "PathIsExecutableAction",
    "PathIsNotExecutableAction",
    "PathIsNotReadableAction",
    "PathIsNotWritableAction",
    "PathIsReadableAction",
    "PathIsValidAction",
    "PathIsWritableAction",
    "ResolvePathAction",
]


class ResolvePathAction(Action):
    """Resolves path to canonical removing symbolic links if present"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Resolve list of paths
            values = [resolve_path(path) for path in values]
        else:
            # Resolve single path
            path = values
            values = resolve_path(path)

        setattr(namespace, self.dest, values)


class EnsureDirectoryAction(Action):
    """Ensure directory exists and create it if it doesnt"""

    @staticmethod
    def _ensure_directory(directory):
        if not is_existing_directory(directory):
            create_directory(directory)

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Ensure list of directories
            [self._ensure_directory(path) for path in values]
        else:
            # Ensure single directory
            path = values
            self._ensure_directory(path)

        setattr(namespace, self.dest, values)


class EnsureFileAction(Action):
    """Ensure file exists and create it if it doesnt"""

    @staticmethod
    def _ensure_file(filename):
        if not is_existing_directory(filename):
            create_file(filename)

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Ensure list of filenames
            [self._ensure_file(path) for path in values]
        else:
            # Ensure single filename
            path = values
            self._ensure_file(path)

        setattr(namespace, self.dest, values)


class PathIsValidAction(Action):
    """Check validity of supplied path(s)"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check validity of list of paths
            if False in [is_valid_path(path) for path in values]:
                raise ValueError(
                    "supplied paths contain atleast one invalid path"
                )
        else:
            # Check validity of single path
            path = values
            if not is_valid_path(path):
                raise ValueError("supplied path is invalid")

        setattr(namespace, self.dest, values)


class PathExistsAction(Action):
    """Check if Path exists"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check validity of list of paths
            if False in [is_existing_path(path) for path in values]:
                raise ValueError(
                    "supplied paths contain atleast one invalid path"
                )
        else:
            # Check validity of single path
            path = values
            if not is_existing_path(path):
                raise ValueError("supplied path is invalid")

        setattr(namespace, self.dest, values)


class PathDoesNotExistsAction(Action):
    """Check if Path does not exist"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check validity of list of paths
            if True in [is_existing_path(path) for path in values]:
                raise ValueError(
                    "supplied paths contain atleast one invalid path"
                )
        else:
            # Check validity of single path
            path = values
            if is_existing_path(path):
                raise ValueError("supplied path is invalid")

        setattr(namespace, self.dest, values)


class PathIsWritableAction(Action):
    """Check if path is writable"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check if list of paths are all writable
            if False in [is_writable_path(path) for path in values]:
                raise ValueError(
                    "supplied files contain atleast one unwritable file"
                )
        else:
            # Check if path is writable
            path = values
            if not is_writable_path(path):
                raise ValueError("supplied file is unwritable")

        setattr(namespace, self.dest, values)


class PathIsNotWritableAction(Action):
    """Check if path is not writable"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check if list of paths are all not  writable
            if True in [is_writable_path(path) for path in values]:
                raise ValueError(
                    "supplied files contain atleast one writable file"
                )
        else:
            # Check if path is not writable
            path = values
            if is_writable_path(path):
                raise ValueError("supplied file is writable")

        setattr(namespace, self.dest, values)


class PathIsReadableAction(Action):
    """Check if path is readable"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check if list of paths are all readable
            if False in [is_readable_path(path) for path in values]:
                raise ValueError(
                    "supplied paths contain atleast one readable path"
                )
        else:
            # Check if path is readable
            path = values
            if not is_readable_path(path):
                raise ValueError("supplied path is readable")

        setattr(namespace, self.dest, values)


class PathIsNotReadableAction(Action):
    """Check if path is not writable"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check if list of paths are all not readable
            if True in [is_readable_path(path) for path in values]:
                raise ValueError(
                    "supplied files contain atleast one readable path"
                )
        else:
            # Check if path is not readable
            path = values
            if is_readable_path(path):
                raise ValueError("supplied path is readable")

        setattr(namespace, self.dest, values)



class PathIsExecutableAction(Action):
    def __init__(self):
        raise NotImplementedError


class PathIsNotExecutableAction(Action):
    def __call__(self):
        raise NotImplementedError


class DirectoryExistsAction(Action):
    """Check if Directory exists"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check existence of list of paths
            if False in [is_existing_directory(path) for path in values]:
                raise ValueError(
                    "supplied paths contain atleast one invalid path"
                )
        else:
            # Check existence of single path
            path = values
            if not is_existing_directory(path):
                raise ValueError("supplied path is invalid")

        setattr(namespace, self.dest, values)


class DirectoryDoesNotExistAction(Action):
    """Check if Directory does not exist"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check existence of list of paths
            if True in [is_existing_directory(path) for path in values]:
                raise ValueError(
                    "supplied paths contain atleast one invalid path"
                )
        else:
            # Check existence of single path
            path = values
            if is_existing_directory(path):
                raise ValueError("supplied path is invalid")

        setattr(namespace, self.dest, values)


class DirectoryIsWritableAction(Action):
    """Check if directory is writable"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check if list of directories are all writable
            if False in [is_writable_directory(path) for path in values]:
                raise ValueError(
                    "supplied dirs contain atleast one unwritable dir"
                )
        else:
            # Check if file is writable
            path = values
            if not is_writable_directory(path):
                raise ValueError("supplied dir is unwritable")

        setattr(namespace, self.dest, values)


class DirectoryIsNotWritableAction(Action):
    """Check if directory is not writable"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check if list of directories are all not writable
            if True in [is_writable_directory(path) for path in values]:
                raise ValueError(
                    "supplied dirs contain atleast one writable dir"
                )
        else:
            # Check if file is not writable
            path = values
            if is_writable_directory(path):
                raise ValueError("supplied dir is writable")

        setattr(namespace, self.dest, values)


class DirectoryIsReadableAction(Action):
    """Check if directory is readable"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check if list of directories are all readable
            if False in [is_readable_directory(path) for path in values]:
                raise ValueError(
                    "supplied dirs contain atleast one readable dir"
                )
        else:
            # Check if directory is readable
            path = values
            if not is_readable_directory(path):
                raise ValueError("supplied dir is dir")

        setattr(namespace, self.dest, values)


class DirectoryIsNotReadableAction(Action):
    """Check if directory is not writable"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check if list of directories are all not readable
            if True in [is_readable_directory(path) for path in values]:
                raise ValueError(
                    "supplied dirs contain atleast one readable dir"
                )
        else:
            # Check if directory is not readable
            path = values
            if is_readable_directory(path):
                raise ValueError("supplied dir is dir")

        setattr(namespace, self.dest, values)


class DirectoryIsExecutableAction(Action):
    def __init__(self):
        raise NotImplementedError


class DirectoryIsNotExecutableAction(Action):
    def __init__(self):
        raise NotImplementedError


class DirectoryIsValidAction(Action):
    """Check validity of supplied dir path(s)"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check validity of list of directory paths
            if False in [is_valid_directory(path) for path in values]:
                raise ValueError(
                    "supplied paths contain atleast one invalid path"
                )
        else:
            # Check validity of single directory path
            path = values
            if not is_valid_directory(path):
                raise ValueError("supplied path is invalid")

        setattr(namespace, self.dest, values)


class FileIsWritableAction(Action):
    """Check if file is writable"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check if list of files are all writable
            if False in [is_writable_file(path) for path in values]:
                raise ValueError(
                    "supplied files contain atleast one unwritable file"
                )
        else:
            # Check if file is writable
            path = values
            if not is_writable_file(path):
                raise ValueError("supplied file is unwritable")

        setattr(namespace, self.dest, values)


class FileIsNotWritableAction(Action):
    """Check if file is not writable"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check if list of files are all not writable
            if True in [is_writable_file(path) for path in values]:
                raise ValueError(
                    "supplied files contain atleast one writable file"
                )
        else:
            # Check if file is not writable
            path = values
            if is_writable_file(path):
                raise ValueError("supplied file is writable")

        setattr(namespace, self.dest, values)


class FileIsReadableAction(Action):
    """Check if file is readable"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check if list of files are all readable
            if False in [is_readable_file(path) for path in values]:
                raise ValueError(
                    "supplied files contain atleast one readable file"
                )
        else:
            # Check if file is readable
            path = values
            if not is_readable_file(path):
                raise ValueError("supplied file is readable")

        setattr(namespace, self.dest, values)


class FileIsNotReadableAction(Action):
    """Check if file is not writable"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check if list of files are all not readable
            if True in [is_readable_file(path) for path in values]:
                raise ValueError(
                    "supplied files contain atleast one readable file"
                )
        else:
            # Check if file is not readable
            path = values
            if is_readable_file(path):
                raise ValueError("supplied file is readable")

        setattr(namespace, self.dest, values)


class FileIsExecutableAction(Action):
    def __init__(self):
        raise NotImplementedError


class FileIsNotExecutableAction(Action):
    def __init__(self):
        raise NotImplementedError


class FileIsValidAction(Action):
    """Check validity of supplied file path(s)"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check validity of list of file paths
            if False in [is_valid_file(path) for path in values]:
                raise ValueError(
                    "supplied file paths contain atleast one invalid file path"
                )
        else:
            # Check validity of single path
            path = values
            if not is_valid_file(path):
                raise ValueError("supplied file path is invalid")

        setattr(namespace, self.dest, values)


class FileExistsAction(Action):
    """Check if File exists"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check existence of list of paths
            if False in [is_existing_file(path) for path in values]:
                raise ValueError(
                    "supplied paths contain atleast one invalid path"
                )
        else:
            # Check existence of single path
            path = values
            if not is_existing_file(path):
                raise ValueError("supplied path is invalid")

        setattr(namespace, self.dest, values)


class FileDoesNotExistAction(Action):
    """Check if File exists"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check existence of list of paths
            if True in [is_existing_file(path) for path in values]:
                raise ValueError(
                    "supplied paths contain atleast one invalid path"
                )
        else:
            # Check existence of single path
            path = values
            if is_existing_file(path):
                raise ValueError("supplied path is invalid")

        setattr(namespace, self.dest, values)


class FileIsEmptyAction(Action):
    def __init__(self):
        raise NotImplementedError


class FileIsNotEmptyAction(Action):
    def __init__(self):
        raise NotImplementedError


class FileHasExtension(Action):
    """Check if file has specified extension

    TODO: Accept extension as an argument

    """

    def __init__(self):
        raise NotImplementedError
