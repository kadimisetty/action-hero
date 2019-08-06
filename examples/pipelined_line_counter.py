import argparse

from action_hero import (
    FileIsReadableAction,
    PipelineAction,
    FilenameHasExtension,
)


if __name__ == "__main__":
    # Create parser
    parser = argparse.ArgumentParser()

    # Add user argument "file"
    # parser.add_argument("--file", action=FileIsReadableAction)
    parser.add_argument(
        "--file",
        action=PipelineAction,
        action_values=[
            (FilenameHasExtension, ["md", "markdown"]),
            FileIsReadableAction,
        ],
    )

    # Parse user arguments
    args = parser.parse_args()

    if args.file:
        # Count lines in file
        with open(args.file) as f:
            # print(f"{args.file} has {len(f.readlines())} lines")
            print("{} has {} lines".format(args.file, len(f.readlines())))
    else:
        # Print usage when no arguments were supplied
        parser.print_usage()
