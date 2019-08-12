from action_hero.utils import (
    CheckPresentInValuesAction,
    DisplayMessageAndExitAction,
    DisplayMessageAndGetInputAction,
    LoadSerializedFile,
)


__all__ = [
    "ChoicesAction",
    "ConfirmAction",
    "GetInputAction",
    "GetSecretInputAction",
    "NotifyAndContinueAction",
    "NotifyAndExitAction",
    "LoadYAMLFromFileAction",
    "LoadJSONFromFileAction",
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


class LoadYAMLFromFileAction(LoadSerializedFile):
    """Return loaded contents of a YAML file"""

    format = "yml"


class LoadJSONFromFileAction(LoadSerializedFile):
    """Return loaded contents of a JSON file"""

    format = "json"
