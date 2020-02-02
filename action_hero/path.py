from action_hero.utils import (
    CheckAction,
    CheckPresentInValuesAction,
    MapAction,
    MapAndReplaceAction,
)
from action_hero.path_utils import (
    create_directory,
    create_file,
    get_extension,
    is_empty_file,
    is_executable_directory,
    is_executable_file,
    is_executable_path,
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
    "FileIsEmptyAction",
    "FileIsExecutableAction",
    "FileIsNotEmptyAction",
    "FileIsNotExecutableAction",
    "FileIsNotReadableAction",
    "FileIsNotWritableAction",
    "FileIsReadableAction",
    "FileIsValidAction",
    "FileIsWritableAction",
    "FileHasExtensionAction",
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


class ResolvePathAction(MapAndReplaceAction):
    """Resolves path to canonical path removing symbolic links if present"""

    func = resolve_path


class EnsureDirectoryAction(MapAction):
    """Ensure directory exists and create it if it doesnt"""

    @staticmethod
    def _ensure_directory(directory):
        # create_directory raises FileExistsError if dir exists so check first
        if not is_existing_directory(directory):
            create_directory(directory)

    func = _ensure_directory


class EnsureFileAction(MapAction):
    """Ensure file exists and create it if it doesnt"""

    @staticmethod
    def _ensure_file(filename):
        if not is_existing_file(filename):
            create_file(filename)

    func = _ensure_file


class PathIsValidAction(CheckAction):
    """Check if path is valid"""

    func = is_valid_path
    error_message = "Invalid path(s)"


class PathExistsAction(CheckAction):
    """Check if path exists"""

    func = is_existing_path
    error_message = "Non-existent path(s)"


class PathDoesNotExistsAction(CheckAction):
    """Check if path does not exist"""

    def func(value):
        return not is_existing_path(value)

    error_message = "Existing path(s)"


class PathIsWritableAction(CheckAction):
    """Check if path is writable"""

    func = is_writable_path
    error_message = "Unwritable path(s)"


class PathIsNotWritableAction(CheckAction):
    """Check if path is not writable"""

    def func(value):
        return not is_writable_path(value)

    error_message = "Writable path(s)"


class PathIsReadableAction(CheckAction):
    """Check if path is readable"""

    func = is_readable_path
    error_message = "Unreadable path(s)"


class PathIsNotReadableAction(CheckAction):
    """Check if path is not writable"""

    def func(value):
        return not is_readable_path(value)

    error_message = "Readable path(s)"


class PathIsExecutableAction(CheckAction):
    """Check if path is executable"""

    func = is_executable_path
    error_message = "Inexecutable path(s)"


class PathIsNotExecutableAction(CheckAction):
    """Check if path is not executable"""

    def func(value):
        return not is_executable_path(value)

    error_message = "Executable path(s)"


class DirectoryExistsAction(CheckAction):
    """Check if directory exists"""

    func = is_existing_directory
    error_message = "Non-existent director(y/ies)"


class DirectoryDoesNotExistAction(CheckAction):
    """Check if directory does not exist"""

    def func(value):
        return not is_existing_directory(value)

    error_message = "Existing director(y/ies)"


class DirectoryIsWritableAction(CheckAction):
    """Check if directory is writable"""

    func = is_writable_directory
    error_message = "Writable director(y/ies)"


class DirectoryIsNotWritableAction(CheckAction):
    """Check if directory is not writable"""

    def func(value):
        return not is_writable_directory(value)

    error_message = "Unwritable director(y/ies)"


class DirectoryIsReadableAction(CheckAction):
    """Check if directory is readable"""

    func = is_readable_directory
    error_message = "Unreadable director(y/ies)"


class DirectoryIsNotReadableAction(CheckAction):
    """Check if directory is not readable"""

    def func(value):
        return not is_readable_directory(value)

    error_message = "Readable director(y/ies)"


class DirectoryIsExecutableAction(CheckAction):
    """Check if directory is executable"""

    func = is_executable_directory
    error_message = "Inexecutable director(y/ies)"


class DirectoryIsNotExecutableAction(CheckAction):
    """Check if directory is not executable"""

    def func(value):
        return not is_executable_directory(value)

    error_message = "Executable director(y/ies)"


class DirectoryIsValidAction(CheckAction):
    """Check directory is valid"""

    func = is_valid_directory
    error_message = "Invalid director(y/ies)"


class FileIsWritableAction(CheckAction):
    """Check if file is writable"""

    func = is_writable_file
    error_message = "Unwritable file(s)"


class FileIsNotWritableAction(CheckAction):
    """Check if file is not writable"""

    def func(value):
        return not is_writable_file(value)

    error_message = "Writable file(s)"


class FileIsReadableAction(CheckAction):
    """Check if file is readable"""

    func = is_readable_file
    error_message = "Unreadable file(s)"


class FileIsNotReadableAction(CheckAction):
    """Check if file is not readable"""

    def func(value):
        return not is_readable_file(value)

    error_message = "Readable file(s)"


class FileIsExecutableAction(CheckAction):
    """Check if file is executable"""

    func = is_executable_file
    error_message = "Inexecutable file(s)"


class FileIsNotExecutableAction(CheckAction):
    """Check if file is not executable"""

    def func(value):
        return not is_executable_file(value)

    error_message = "Executable file(s)"


class FileIsValidAction(CheckAction):
    """Check file is valid"""

    func = is_valid_file
    error_message = "Valid file(s)"


class FileExistsAction(CheckAction):
    """Check if file exists"""

    func = is_existing_file
    error_message = "Non-existent file(s)"


class FileDoesNotExistAction(CheckAction):
    """Check if file exists"""

    def func(value):
        return not is_existing_file(value)

    error_message = "Existing file(s)"


class FileIsEmptyAction(CheckAction):
    """Check if file is empty"""

    func = is_empty_file
    error_message = "Non-empty file(s)"


class FileIsNotEmptyAction(CheckAction):
    """Check if file is not empty"""

    def func(value):
        return not is_empty_file(value)

    error_message = "Empty file(s)"


class FileHasExtensionAction(CheckPresentInValuesAction):
    """Check if file has specified extension"""

    func = get_extension
    error_message = "File(s) with unexpected extensions"
