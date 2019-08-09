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
    error_message = "Value(s) not convertible to int"


class IsConvertibleToFloatAction(CheckAction):
    """Check if value is convertible to float"""

    func = is_convertible_to_float
    error_message = "Value(s) not convertible to float"


class IsTruthyAction(CheckAction):
    """Checks if value is truthy"""

    func = is_truthy
    error_message = "Value(s) is not truthy"


class IsFalsyAction(CheckAction):
    """Checks if value is falsy"""

    def func(value):
        return not is_truthy(value)

    error_message = "Value(s) is not falsy"


class IsConvertibleToUUIDAction(CheckAction):
    """Checks if value is convertible to UUID"""

    func = is_convertible_to_UUID
    error_message = "Value(s) not convertible to UUID"
