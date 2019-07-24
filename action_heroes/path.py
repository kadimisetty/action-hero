import argparse


# TODO
# Files:
# - Specific Format/Extension
# - With Number of Lines
# - Specific Encoding


class ValidPathAction(argparse.Action):
    pass


class ExistingDirectoryAction(argparse.Action):
    pass


class NonExistingDirectoryAction(argparse.Action):
    pass


class WritableDirectoryAction(argparse.Action):
    pass


class UnWritableDirectoryAction(argparse.Action):
    pass


class ReadableDirectoryAction(argparse.Action):
    pass


class UnReadableDirectoryAction(argparse.Action):
    pass


class ExecutableDirectoryAction(argparse.Action):
    pass


class UnExecutableDirectoryAction(argparse.Action):
    pass


class ValidDirectoryAction(argparse.Action):
    pass


class WritableFileAction(argparse.Action):
    pass


class UnWritableFileAction(argparse.Action):
    pass


class ReadableFileAction(argparse.Action):
    pass


class UnReadableFileAction(argparse.Action):
    pass


class ExecutableFileAction(argparse.Action):
    pass


class UnExecutableFileAction(argparse.Action):
    pass


class ValidFileAction(argparse.Action):
    pass


class ExistingFileAction(argparse.Action):
    pass


class NonExistingFileAction(argparse.Action):
    pass


class EmptyFileAction(argparse.Action):
    pass


class NonEmptyFileAction(argparse.Action):
    pass
