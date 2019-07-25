from argparse import Action

from action_heroes.path_utils import (
    create_directory,
    create_file,
    is_existing_directory,
    is_valid_file,
    is_valid_path,
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
    pass


class PathDoesNotExistsAction(Action):
    pass


class PathIsWritableAction(Action):
    pass


class PathIsNotWritableAction(Action):
    pass


class PathIsReadableAction(Action):
    pass


class PathIsNotReadableAction(Action):
    pass


class PathIsExecutableAction(Action):
    pass


class PathIsNotExecutableAction(Action):
    pass


class DirectoryExistsAction(Action):
    pass


class DirectoryDoesNotExistAction(Action):
    pass


class DirectoryIsWritableAction(Action):
    pass


class DirectoryIsNotWritableAction(Action):
    pass


class DirectoryIsReadableAction(Action):
    pass


class DirectoryIsNotReadableAction(Action):
    pass


class DirectoryIsExecutableAction(Action):
    pass


class DirectoryIsNotExecutableAction(Action):
    pass


class FileIsWritableAction(Action):
    pass


class FileIsNotWritableAction(Action):
    pass


class FileIsReadableAction(Action):
    pass


class FileIsNotReadableAction(Action):
    pass


class FileIsExecutableAction(Action):
    pass


class FileIsNotExecutableAction(Action):
    pass


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
    pass


class FileDoesNotExistAction(Action):
    pass


class FileIsEmptyAction(Action):
    pass


class FileIsNotEmptyAction(Action):
    pass


class FileHasExtension(Action):
    pass
