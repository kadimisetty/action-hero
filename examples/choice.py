import argparse

from action_hero import ChoicesAction


if __name__ == "__main__":
    # Create parser
    parser = argparse.ArgumentParser()

    # Add user argument "file"
    parser.add_argument(
        "--color",
        action=ChoicesAction,
        nargs="+",
        action_values=["red", "blue", "green"],
    )

    # Parse user arguments
    args = parser.parse_args()

    if args:
        # Show args
        print(args)
    else:
        # Print usage when no arguments were supplied
        parser.print_usage()
