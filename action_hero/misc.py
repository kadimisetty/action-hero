from action_hero.utils import (
    CheckPresentInValuesAction,
    CollectIntoContainerAction,
    DisplayMessageAndExitAction,
    DisplayMessageAndGetInputAction,
    LoadSerializedFileAction,
)


__all__ = [
    "ChoicesAction",
    "CollectIntoDictAction",
    "CollectIntoListAction",
    "CollectIntoTupleAction",
    "ConfirmAction",
    "GetInputAction",
    "GetSecretInputAction",
    "LoadJSONFromFileAction",
    "LoadPickleFromFileAction",
    "LoadYAMLFromFileAction",
    "NotifyAndContinueAction",
    "NotifyAndExitAction",
]


class ChoicesAction(CheckPresentInValuesAction):
    """Limit options to provided choices"""

    def func(value):
        return value

    error_message = "Value(s) not in allowed choices"


class NotifyAndContinueAction(DisplayMessageAndExitAction):
    """Display message from action_value(s) and continue"""

    exit = False


class NotifyAndExitAction(DisplayMessageAndExitAction):
    """Display message from action_value(s) and exit"""

    exit = True


class ConfirmAction(DisplayMessageAndExitAction):
    """Display message from action_value(s) and continue on confirmation"""

    get_confirmation = True
    exit = False


class GetInputAction(DisplayMessageAndGetInputAction):
    """Get input and save to `self.dest` """

    hide_input_on_screen = False


class GetSecretInputAction(DisplayMessageAndGetInputAction):
    """Get input and save to `self.dest` while hiding characters from screen"""

    hide_input_on_screen = True


class LoadYAMLFromFileAction(LoadSerializedFileAction):
    """Return loaded contents of a YAML file"""

    format = "yaml"


class LoadJSONFromFileAction(LoadSerializedFileAction):
    """Return loaded contents of a JSON file"""

    format = "json"


class LoadPickleFromFileAction(LoadSerializedFileAction):
    """Return loaded contents of a JSON file"""

    format = "pickle"


class CollectIntoListAction(CollectIntoContainerAction):
    """Collect into a list and return it"""

    collector = list


class CollectIntoTupleAction(CollectIntoContainerAction):
    """Collect into a tuple and return it"""

    collector = tuple


class CollectIntoDictAction(CollectIntoContainerAction):
    """Collect into dict and return it"""

    collector = dict
