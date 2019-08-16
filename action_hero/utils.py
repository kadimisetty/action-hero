import argparse
import contextlib
import functools
import getpass
import io
import json
import pickle
import sys
import unittest
import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


import requests


__all__ = [
    "ActionHeroAction",
    "CheckAction",
    "CheckPresentInValuesAction",
    "CollectIntoContainerAction",
    "DebugAction",
    "DisplayMessageAndExitAction",
    "DisplayMessageAndGetInputAction",
    "LoadSerializedFileAction",
    "MapAction",
    "MapAndReplaceAction",
    "PipelineAction",
    "capture_output",
    "run_only_when_modules_loaded",
    "run_only_when_when_internet_is_up",
]


def capture_output(func, *args):
    """Return captured stdout output of func when called"""
    stdout = io.StringIO()

    # Context manager to fetch all stdout output into value stdoout
    with contextlib.redirect_stdout(stdout):
        func(*args)

    # Return sanitized stdout output value of func
    return stdout.getvalue().strip()


def run_only_when_modules_loaded(modules=["argparse"]):
    """Decorator that runs wrapped function only when the supplied modules are
    loaded

    Args:
        modules (list[srtr]): List of modules to check if loaded

    """

    def run_only_when_modules_loaded_wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Only run func if module loaded
            if all([(module in sys.modules) for module in modules]):
                func(*args, **kwargs)

        return wrapper

    return run_only_when_modules_loaded_wrapper


def run_only_when_when_internet_is_up(urls=["http://www.google.com"]):
    """Decorator that runs wrapped function when the internet is up.

    Connection is checked by checking connection to values in urls

    Args:
        urls (list[str]): List of urls to check for when checking for
        connection

    """

    def run_only_when_when_internet_is_up_wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Do network check
            try:
                [requests.get(url).raise_for_status() for url in urls]

                func(*args, **kwargs)

            # Do nothing on response error
            except requests.exceptions.RequestException:
                pass

        return wrapper

    return run_only_when_when_internet_is_up_wrapper


class ActionHeroAction(argparse.Action):
    pass


class BaseAction(ActionHeroAction):
    """ArgumentParser Action subclass that runs user's func over values

    ActionHero' Baseclass for subclasses that need access to a func and
        error_message

    Attributes:
        func (func): To be used to fill in subclasses preferred func.
        error_message(str): Message used to report errors

    """

    func = None
    error_message = None

    @classmethod
    def _run_user_func(cls, value):
        """Runs cls.func over value

        Used nside __call__

        Needs to be @classmethod to avoid
        1. including self when being called in other methods
        2. not including self when calling other funcs within

        Args:
            cls (cls): classmethod argument
            value (type): The value to run cls.func upon

        """
        return cls.func(value)


class CheckAction(BaseAction):
    """Checks all values return True with func. Args from superclass
    argparse.Action

    """

    def __init__(
        self, option_strings, dest, nargs=None, help=None, metavar=None
    ):
        for attr in ["func", "error_message"]:
            # Use getattr. hasattr returns True as they're initialized to None.
            if not getattr(self, attr):
                raise ValueError(
                    "Please supply required attribute: {}".format(attr)
                )

        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            help=help,
            metavar=metavar,
        )

    def __call__(self, parser, namespace, values, option_string=None):
        # When values are a list of strings
        if isinstance(values, list):
            failures = [
                value for value in values if not self._run_user_func(value)
            ]

            if failures:
                raise argparse.ArgumentError(
                    self,
                    "{}: {}".format(self.error_message, ", ".join(failures)),
                )

        # When values is one string
        else:
            value = values
            if not self._run_user_func(value):
                failure = value
                raise argparse.ArgumentError(
                    self, "{}: {}".format(self.error_message, failure)
                )

        setattr(namespace, self.dest, values)


class CheckPresentInValuesAction(BaseAction):
    """Checks result func over each value in values is in action_values.

    Args from main superclass argparse.Action

    Attributes:
        action_values (list[str]): List of strings to accept as values used to
            check presence in with results of func attribute.

    """

    action_values = None

    def __init__(
        self,
        option_strings,
        dest,
        action_values=None,
        nargs=None,
        type=None,
        help=None,
        metavar=None,
    ):
        for attr in ["func", "error_message"]:
            # Use getattr. hasattr returns True as they're initialized to None.
            if not getattr(self, attr):
                raise ValueError(
                    "Please supply required attribute: {}".format(attr)
                )

        # Raise exception if action_values are invalid, else accept
        _raise_exception_if_invalid_action_values(
            action_values=action_values,
            container_type=list,
            empty_allowed=False,
            different_item_types_allowed=False,
            preferred_exception=ValueError,
        )
        self.action_values = action_values

        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            type=type,
            help=help,
            metavar=metavar,
        )

    def __call__(self, parser, namespace, values, option_string=None):

        # 1. Check presence

        # 1.1 Check if something other than default type was given Do type
        #   conversion of value in values
        # self.type is set when type is passed in with add_argument, else str
        default_type = str
        chosen_type = self.type if self.type else default_type
        # Check all action_value are of specified type passed with add_argument
        if not all([type(v) is chosen_type for v in self.action_values]):
            raise ValueError(
                "Items in action_values should be of given type {}".format(
                    chosen_type
                )
            )

        # 1.2 Check presence for every value in values
        if isinstance(values, list):
            failures = [
                value
                for value in values
                if self._run_user_func(chosen_type(value))
                not in self.action_values
            ]

            if failures:
                raise argparse.ArgumentError(
                    self,
                    "{}: {}".format(self.error_message, ", ".join(failures)),
                )

        # 1.3 Check presence for values
        else:
            value = values
            if (
                not self._run_user_func(chosen_type(value))
                in self.action_values
            ):
                failure = value
                raise argparse.ArgumentError(
                    self, "{}: {}".format(self.error_message, failure)
                )
                raise argparse.ArgumentError(self, self.error_message)

        setattr(namespace, self.dest, values)


class MapAction(BaseAction):
    """Maps func on values. Args from main suoperclass argparse.Action."""

    def __init__(
        self, option_strings, dest, nargs=None, help=None, metavar=None
    ):
        for attr in ["func"]:
            # Use getattr. hasattr returns True as they're initialized to None.
            if not getattr(self, attr):
                raise ValueError(
                    "Please supply required attribute: {}".format(attr)
                )

        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            help=help,
            metavar=metavar,
        )

    def __call__(self, parser, namespace, values, option_string=None):
        # When values are a list of strings
        if isinstance(values, list):
            [self._run_user_func(value) for value in values]

        # When values is one string
        else:
            value = values
            self._run_user_func(value)

        setattr(namespace, self.dest, values)


class MapAndReplaceAction(BaseAction):
    """Maps func on values and replaces values with the result. Args from main
    superclass argparse.Action"""

    def __init__(
        self, option_strings, dest, nargs=None, help=None, metavar=None
    ):
        for attr in ["func"]:
            # Use getattr. hasattr returns True as they're initialized to None.
            if not getattr(self, attr):
                raise ValueError(
                    "Please supply required attribute: {}".format(attr)
                )

        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            help=help,
            metavar=metavar,
        )

    def __call__(self, parser, namespace, values, option_string=None):
        # When values are a list of strings
        if isinstance(values, list):
            updated = [self._run_user_func(value) for value in values]
            values = updated

        # When values is one string
        else:
            value = values
            updated = self._run_user_func(value)
            values = updated

        setattr(namespace, self.dest, values)


class PipelineAction(ActionHeroAction):
    """Run ActionHero actions thrugh a pipeline.

    Actions that are run through a pipeline need to satify two constraints:
        1. Technical: Type need to match betwen piping and pipee actions.
        2. Logical: Piping some actions might not make logical sense.
            e.g. FilexxxActions to URLxxxActions

    Known Issues with Testing:
        Cases when the parser has pipeline action with multiple action_values
        due to the way argumenterrors are raised and exits.  Current workaround
        solution is to run those particular tests in a subprocess.  Note that
        this workaround WILL ONLY WORK when action_hero module is available
        e.g. with `pip install --editable .` which might not be the case on a
        different system. e.g. a CI system where action_hero module is not
        loaded.

    Attributes:
        children (list): Valid action_hero actions to pipeline through.
            Order of children is to be preserved.
        action_values (list[Action/(Action, [str])): Action values to this
            class contains a list of one of two valid options:
                1. [action_hero action]
                2. Tuple of (action_hero action, action_values<list>)

    """

    children = []
    action_values = None

    @staticmethod
    def _is_valid_action_hero_action(action):
        return issubclass(action, ActionHeroAction)

    def __init__(
        self,
        option_strings,
        dest,
        action_values=None,
        nargs=None,
        help=None,
        metavar=None,
    ):

        # Raise exception if action_values are invalid, else accept
        _raise_exception_if_invalid_action_values(
            action_values=action_values,
            container_type=list,
            empty_allowed=False,
            different_item_types_allowed=True,
            preferred_exception=ValueError,
        )
        self.action_values = action_values

        # Add actions as children
        for value in self.action_values:
            # Form 1 tuple of action class and it's action_values
            if isinstance(value, tuple):
                # 1. Get action class and action_values
                action = value[0]
                action_values = value[1]

                # 2. Verify the action is legit and raise ValueError if not
                if not self._is_valid_action_hero_action(action):
                    raise ValueError(
                        "Invalid action_hero action: {}".format(action)
                    )
                else:
                    # 3. Add action to children
                    self.children.append(
                        action(
                            option_strings=option_strings,
                            dest=dest,
                            nargs=nargs,
                            action_values=action_values,
                            help=help,
                            metavar=metavar,
                        )
                    )

            # Form 2 is an action class
            elif issubclass(value, argparse.Action):
                # 1. Get action class
                action = value
                # 2. Verify the action is legit and raise ValueError if not
                if not self._is_valid_action_hero_action(action):
                    raise ValueError(
                        "Invalid action_hero action: {}".format(action)
                    )
                # 3. Add action to children
                self.children.append(
                    action(
                        option_strings=option_strings,
                        dest=dest,
                        nargs=nargs,
                        help=help,
                        metavar=metavar,
                    )
                )

            # Raise ValueError if unexpected value
            else:
                raise ValueError("action_values contains invalid values")

        # REMAINDER PIPELINE INIT
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            help=help,
            metavar=metavar,
        )

    def __call__(self, parser, namespace, values, option_string=None):
        """Call each child action within PipelineAction's __call__

        All actions are called inside PipelineAction's namespace, thus end up
        using similar attributes such as namespace, parser etc. and as they
        each get called one after the other, they replace dest with their
        result. Thus they end up piping through results via `dest` in this
        namespace.

        No need to call setattr(namespace, self.dest, values) here, because
        we'll be leaving the result of the last action in the pipeline as it
        is and PipeineAction doesnt make any namespace changes

        """
        for child in self.children:
            child(
                parser=parser,
                namespace=namespace,
                values=values,
                option_string=option_string,
            )


class ExitCapturedArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        """error(message: string)

        Important note from this superclass's error(s, m) docstring:
            If you override this in a subclass, it should not return -- it
            should either exit or raise an exception.

        Reason for overriding superclass error:
            This function is overridden in order to stop the default behavior
            of ArgumentParser to exit when receiving an ArgumentError as that
            convolutes testing.
            So instead of exiting, just constructing the message and passing it
            on as a ValueError that can be captured in testing.

        Args:
            message(str): Use to explain reason for error.

        Raises:
            ValueError: Raises valueerror with formatted message.
        """
        error_message = "{}s: error: {}s\n".format(self.prog, message)
        raise ValueError(error_message)


class ActionHeroTestCase(unittest.TestCase):
    """unitests.TestCase subclass that encloses a ExitCapturedArgumentParser

    Reason for a special TestCase:
        1. Enclose parser within setup
        2. The enclosed parser should capture exits and raise ValueError

    """

    def setUp(self):
        """Enclose ExitCapturedArgumentParser as parser"""
        self.parser = ExitCapturedArgumentParser()


def _raise_exception_if_invalid_action_values(
    action_values=None,
    container_type=list,
    empty_allowed=False,
    different_item_types_allowed=False,
    preferred_exception=ValueError,
):
    """Raise an exception if supplied action_values are deemed invalid


    Args:
        action_values (list): aciton_values to check validity for
        container_type (list): container type of action_Values
        empty_allowed(bool): Whether action_values is allowed to be emoty
        preferred_exception(Exception): preferred exception to call to raise an
            error

    """

    # Raise exception if action_values is still None
    if action_values is None:
        raise preferred_exception(
            "Please supply required attribute: action_values"
        )

    # Non-empty action_values
    else:
        # Raise exception if action_values is not of container type
        if not isinstance(action_values, container_type):
            raise preferred_exception(
                "action_values has to be of type: {}".format(container_type)
            )

        # Raise exception if action_values list is empty
        # and empty not allowed
        elif len(action_values) == 0:
            if not empty_allowed:
                raise preferred_exception(
                    "Required attribute action_values cannot be empty list"
                )

        # Raise exception if action_values list has different types
        # and different item types not allowed
        else:

            def has_different_types_of_items(l):
                return len(set([v.__class__ for v in l])) != 1

            if has_different_types_of_items(action_values):
                if not different_item_types_allowed:
                    raise preferred_exception(
                        "Items in this action's action_values should all "
                        "have the same type"
                    )


class DisplayMessageAndExitAction(BaseAction):
    """Display message from action_values and confirm and exit if wanted"""

    action_values = None

    get_confirmation = False
    exit = False

    def __init__(
        self,
        option_strings,
        dest,
        action_values=None,
        nargs=None,
        type=None,
        help=None,
        metavar=None,
    ):

        # Raise exception if action_values are invalid, else accept
        _raise_exception_if_invalid_action_values(
            action_values=action_values,
            container_type=list,
            empty_allowed=False,
            different_item_types_allowed=False,
            preferred_exception=ValueError,
        )
        self.action_values = action_values

        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            type=type,
            help=help,
            metavar=metavar,
        )

    def __call__(self, parser, namespace, values, option_string=None):

        # 1. CONFIRMATION (Exit program if confirmation is no)
        if self.get_confirmation:

            # 2.1 If single message in action_values, append confirmation
            # prompt at  end of message
            if len(self.action_values) == 1:
                message = self.action_values[0]
                # Exit program, if any other key than y ot Y
                if input("{} [Yn] ".format(message)).lower() != "y":
                    sys.exit()

            # 2.2 If multiple messages in action_values, show confirmation
            # prompt on line after
            else:
                [print(message) for message in self.action_values]
                # Exit program, if any other key than y ot Y
                if input("[Yn] ").lower() != "y":
                    sys.exit()

        # 2. DISPLAY MESSAGE(S) ONLY
        else:
            [print(value) for value in self.action_values]

            # Exit program when specified, else continue
            if self.exit:
                sys.exit()


class DisplayMessageAndGetInputAction(BaseAction):
    """
    Display message from action_values, get input and save to `self.dest`

    Attributes:
        action_values([str]): Values to be passed to this Action.
            List of messages to display
        hide_input_on_screen(bool): Whether to hide input like a password

    Note:
        This is a desctructive Action. It replaces the value of dest as single
        str with input.

        Due to dependence on getpass, this will only work on terminals.

        By default saves as type, str.
        TODO: Accoomodate self.type .e.g for type=int, convert to type

    """

    action_values = None

    hide_input_on_screen = False

    def __init__(
        self,
        option_strings,
        dest,
        action_values=None,
        nargs=None,
        type=None,
        help=None,
        metavar=None,
    ):

        # Raise exception if action_values are invalid, else accept
        _raise_exception_if_invalid_action_values(
            action_values=action_values,
            container_type=list,
            empty_allowed=False,
            different_item_types_allowed=False,
            preferred_exception=ValueError,
        )
        self.action_values = action_values

        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            type=type,
            help=help,
            metavar=metavar,
        )

    def __call__(self, parser, namespace, values, option_string=None):

        # 1. Display any provided message prompts for input from action_values
        display_message = "\n".join(
            [message for message in self.action_values]
        )
        display_message += " : "

        try:
            # 2. If self.hide_input_on_screen
            if self.hide_input_on_screen:
                # 2.1 Get user input (while hiding characters)
                values = getpass.getpass(display_message)

            # 2. If not self.hide_input_on_screen
            else:
                # 2.2 Get user input
                values = input(display_message)

        # Don't alter values on keyboard interrupt
        except KeyboardInterrupt:
            print("<Input Cancelled>")

        setattr(namespace, self.dest, values)


class DebugAction(BaseAction):
    """Prints debug information"""

    def __call__(self, parser, namespace, values, option_string=None):

        # BEGIN
        print("┌─────────┐")
        print("│  DEBUG  │")
        print("├─────────┴─────────")

        attributes = [
            "{}: {}".format(attribute, getattr(self, attribute))
            # Get all attributes from dir(self) i.e. self.__dict__
            for attribute in dir(self)
            # Remove callables. Use getattr to check using self.attribute
            if not callable(getattr(self, attribute))
            # Remove dunders
            and not (attribute.startswith("__") and attribute.endswith("__"))
            # Remove private attributes
            and not (attribute.startswith("_"))
        ]

        [print("│ {}".format(attribute)) for attribute in attributes]

        print("├───────────────────")

        # namespace
        print("│ {}".format(namespace))

        # values type and values
        if isinstance(values, list):
            # values is a list
            print("│ values(list): {}".format(values))

        else:
            # values is a str
            print("│ values(str): {}".format(values))

        # option_string
        if option_string:
            print("│ option_string: {}".format(option_string))

        print("└───────────────────")


class LoadSerializedFileAction(BaseAction):
    """Load YAML/JSON file

    Args:
        format(str): the format (YAML/JSON) to load file as

    """

    format = None

    def load_json_from_file(self, file):
        """Return loaded json file

        Args:
            file(str/path): Filename to load json from

        Returns:
            (dict/list): contents of json file

        Raises:
            argparse.ArgmentError that captures json.JSONDecodeError: When the
                loaded json cannot be decoded

        """
        try:
            with open(file, "r") as f:
                return json.load(f)

        except json.JSONDecodeError as e:
            raise argparse.ArgumentError(
                self, "JSONDecodeError in file {}: {}".format(file, e)
            )

    def load_yaml_from_file(self, file):
        """Return loaded yaml file

        Args:
            file(str/path): Filename to load yaml from

        Returns:
            (list/dict): contents of yaml file

        Raises:
            argparse.ArgmentError that captures yaml.YAMLError: When the
                yaml cannot be loaded

        """
        try:
            with open(file) as f:
                return yaml.load(f, Loader=Loader)

        except yaml.YAMLError as e:
            if hasattr(e, "problem_mark"):
                # Report point of problem
                mark = e.problem_mark
                raise argparse.ArgumentError(
                    "Error position: (%s:%s)"
                    % (mark.line + 1, mark.column + 1)
                )
            else:
                raise argparse.ArgumentError(
                    "Error in configuration file: {}".format(e)
                )

    def load_pickle_from_file(self, file):
        """Return loaded pickle file

        Args:
            file(str/path): Filename to load pickled data from

        Returns:
            (list/dict): contents of pickle file

        Raises:
            argparse.ArgmentError that captures yaml.YAMLError: When the
                yaml cannot be loaded

        """
        try:
            with open(file, "rb") as f:
                return pickle.load(f)

        except pickle.UnpicklingError as e:
            raise argparse.ArgumentError(self, e)

        except (
            AttributeError,
            EOFError,
            ImportError,
            IndexError,
            pickle.PickleError,
        ) as e:
            raise argparse.ArgumentError(self, "Unable to unpickle: {}", e)

    def __call__(self, parser, namespace, values, option_string=None):
        loader_for_format = {
            "json": self.load_json_from_file,
            "yaml": self.load_yaml_from_file,
            "pickle": self.load_pickle_from_file,
        }

        # Verify self.format was supplied
        if not self.format:
            raise ValueError("Required file format not specified")

        # Verify there is a loader present for self.format
        elif self.format not in loader_for_format:
            raise ValueError(
                "Unsupported file format: {}. Supported format(s): {}".format(
                    self.format,
                    ", ".join(
                        [format for format in list(loader_for_format.keys())]
                    ),
                )
            )

        # Run loader and save to self.dest
        else:
            # When values is a list
            if isinstance(values, list):
                values = [
                    loader_for_format[self.format](value) for value in values
                ]

            # When values is a str
            else:
                value = values
                value = loader_for_format[self.format](value)
                values = value

            # Save to self.dest
            setattr(namespace, self.dest, values)


class CollectIntoContainerAction(BaseAction):
    """Collect into container of specified type and return it

    Args:
        collector(str): the container(list/tuple/dict) to collect into

    """

    action_values = None
    collector = None

    def __init__(
        self,
        option_strings,
        dest,
        action_values=None,
        nargs=None,
        type=None,
        help=None,
        metavar=None,
    ):

        # Accept action_values but only do verification within dict
        # collector, because it's the only collector that uses action_values
        # currently
        if action_values:
            self.action_values = action_values

        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            type=type,
            help=help,
            metavar=metavar,
        )

    @staticmethod
    def collect_into_list(values):
        """Return collected values into a list"""
        return list(values)

    @staticmethod
    def collect_into_tuple(values):
        """Return collected values into a tuple"""
        return tuple(values)

    def collect_into_dict(self, values):
        """Return collected values into a dict"""
        # 1. Verify delimiter was supplied and is of type str
        # - Raise exception if action_values are invalid, else accept
        # - Container type is str to accept single delimiter
        _raise_exception_if_invalid_action_values(
            action_values=self.action_values,
            container_type=list,
            empty_allowed=False,
            different_item_types_allowed=False,
            preferred_exception=ValueError,
        )
        self.action_values

        # Get delimiters from action_values
        delimiters = self.action_values

        # 2. Verify delimiter is present in all values
        failures = [
            value
            for value in values
            if not any([delimiter in value for delimiter in delimiters])
        ]
        if failures:
            raise argparse.ArgumentError(
                self,
                'Delimiter(s) "{}" not present in: {}'.format(
                    ", ".join(delimiters), ", ".join(failures)
                ),
            )

        # 3. Return a dict with collected kv(key, value) pairs
        d = {}
        for value in values:
            # Search for first found delimiter to split on
            for delimiter in delimiters:
                # At this point, it is verified there is atleast one delimiter
                # present, so loop until it is found
                # Extract key, value pairs by splitting on first present
                # delimiter
                if delimiter in value:
                    # Save (key, value) pair into dict to return
                    (key, value) = tuple(value.split(delimiter))
                    d[key] = value

                    # Exit for loop if first delimiter is found
                    break
        return d

    def __call__(self, parser, namespace, values, option_string=None):
        collectors = {
            list: self.collect_into_list,
            tuple: self.collect_into_tuple,
            dict: self.collect_into_dict,
        }

        # 1. Verify supplied collector is supported
        if self.collector not in collectors:
            "Unsupported container: {}. Supported container(s): {}".format(
                self.collector, ", ".join(str(collectors.keys()))
            )

        # 2. Ensure values is a list
        if not isinstance(values, list):
            values = list(values)

        # 3. Collect into container
        values = collectors[self.collector](values)

        # 4. Save to self.dest
        setattr(namespace, self.dest, values)
