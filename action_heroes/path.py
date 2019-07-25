from argparse import Action


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
    "EnsurePathAction",
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
    pass


class EnsurePathAction(Action):
    pass


class EnsureDirectoryAction(Action):
    pass


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
