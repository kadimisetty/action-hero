from action_hero.utils import (
    CheckPresentInValuesAction,
    DisplayMessageAndExitAction,
)


__all__ = [
    "ChoicesAction",
    "ConfirmAction",
    "NotifyAndContinueAction",
    "NotifyAndExitAction",
]


class ChoicesAction(CheckPresentInValuesAction):
    """Limit options to provided choices"""

    def func(value):
        return value

    err_msg_singular = "Value is not present in valid choices."
    err_msg_plural = "Atleast one value is not present in valid choices."


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
