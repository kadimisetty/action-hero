from action_hero.utils import CheckPresentInValuesAction


__all__ = ["ChoicesAction"]


class ChoicesAction(CheckPresentInValuesAction):
    """Limit options to provided choices"""

    def func(value):
        return value

    err_msg_singular = "Value is not present in valid choices."
    err_msg_plural = "Atleast one value is not present in valid choices."
