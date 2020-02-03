import argparse

from action_hero import FileIsReadableAction


if __name__ == "__main__":

    # Create parser
    parser = argparse.ArgumentParser()

    # Add user argument "--file" and confirm that it will be readable
    parser.add_argument("--file", action=FileIsReadableAction)

    # Parse user arguments
    args = parser.parse_args()

    if args.file:
        # Print number of lines in file
        with open(args.file) as f:
            print("{} has {} lines".format(args.file, len(f.readlines())))
    else:
        # Print usage if no arguments were given
        parser.print_usage()
