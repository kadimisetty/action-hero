import sys
import unittest
import functools
import argparse

import requests


__all__ = [
    "ActionHeroAction",
    "CheckAction",
    "CheckPresentInValuesAction",
    "MapAction",
    "MapAndReplaceAction",
    "PipelineAction",
    "run_only_when_modules_loaded",
    "run_only_when_when_internet_is_up",
]


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

    ActionHero' Baseclass for subclasses that need access to a func,
        err_msg_singular and err_msg_plural

    Attributes:
        func (func): To be used to fill in subclasses preferred func.
        err_msg_singular(str): To be used to fill error message for singular
            failure.
        err_msg_plural(str): To be used to fill error message for singular
            failure.

    """

    func = None
    err_msg_singular = None
    err_msg_plural = None

    @classmethod
    def run_user_func(cls, value):
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
        for attr in ["func", "err_msg_singular", "err_msg_plural"]:
            # Use getattr. hasattr returns True as they're initialized to None.
            if not getattr(self, attr):
                raise ValueError(
                    "Please supply required attribute: {}".format(attr)
                )

        super(CheckAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            help=help,
            metavar=metavar,
        )

    def __call__(self, parser, namespace, values, option_string=None):
        # When values are a list of strings
        if isinstance(values, list):
            if not all([self.run_user_func(value) for value in values]):
                raise argparse.ArgumentError(self, self.err_msg_plural)

        # When values is one string
        else:
            value = values
            if not self.run_user_func(value):
                raise argparse.ArgumentError(self, self.err_msg_singular)

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
        for attr in ["func", "err_msg_singular", "err_msg_plural"]:
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

        super(CheckPresentInValuesAction, self).__init__(
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
                "items in action_values should be of given type {}".format(
                    chosen_type
                )
            )

        # 1.2 Check presence for every value in values
        if isinstance(values, list):
            if not all(
                [
                    self.run_user_func(chosen_type(value))
                    in self.action_values
                    for value in values
                ]
            ):
                raise argparse.ArgumentError(self, self.err_msg_plural)

        # 1.3 Check presence for values
        else:
            value = values
            if (
                not self.run_user_func(chosen_type(value))
                in self.action_values
            ):
                raise argparse.ArgumentError(self, self.err_msg_singular)

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

        super(MapAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            help=help,
            metavar=metavar,
        )

    def __call__(self, parser, namespace, values, option_string=None):
        # When values are a list of strings
        if isinstance(values, list):
            [self.run_user_func(value) for value in values]

        # When values is one string
        else:
            value = values
            self.run_user_func(value)

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

        super(MapAndReplaceAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            help=help,
            metavar=metavar,
        )

    def __call__(self, parser, namespace, values, option_string=None):
        # When values are a list of strings
        if isinstance(values, list):
            updated = [self.run_user_func(value) for value in values]
            values = updated

        # When values is one string
        else:
            value = values
            updated = self.run_user_func(value)
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
        super(PipelineAction, self).__init__(
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
                "Required attribute action_values has to be of type list"
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
