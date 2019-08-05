from action_hero.utils import CheckAction

from action_hero.types_utils import (
    is_convertible_to_int,
    is_convertible_to_float,
    is_convertible_to_UUID,
    is_truthy,
)


__all__ = [
    "IsConvertibleToFloatAction",
    "IsConvertibleToIntAction",
    "IsConvertibleToUUIDAction",
    "IsFalsyAction",
    "IsTruthyAction",
]


class IsConvertibleToIntAction(CheckAction):
    """Check if value is convertible to int"""

    func = is_convertible_to_int
    err_msg_singular = "Value is not convertible to int"
    err_msg_plural = "Atleast one value is not convertible to int"


class IsConvertibleToFloatAction(CheckAction):
    """Check if value is convertible to float"""

    func = is_convertible_to_float
    err_msg_singular = "Value is not convertible to float"
    err_msg_plural = "Atleast one value is not convertible to float"


class IsTruthyAction(CheckAction):
    """Checks if value is truthy"""

    func = is_truthy
    err_msg_singular = "Value is falsy"
    err_msg_plural = "Atleast one value is falsy"


class IsFalsyAction(CheckAction):
    """Checks if value is falsy"""

    def func(value):
        return not is_truthy(value)

    err_msg_singular = "value is falsy"
    err_msg_plural = "Atleast one value is falsy"


class IsConvertibleToUUIDAction(CheckAction):
    """Checks if value is convertible to UUID"""

    func = is_convertible_to_UUID
    err_msg_singular = "Value cannot be converted to UUID"
    err_msg_plural = "Atleast one value cannot be converted to UUID"
