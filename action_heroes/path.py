from argparse import Action

from action_heroes.path_utils import (
    create_directory,
    is_existing_directory,
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
    pass


class PathIsValidAction(Action):
    pass


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
    pass


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
