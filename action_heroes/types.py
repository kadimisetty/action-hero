from argparse import Action

from action_heroes.types_utils import (
    is_convertible_to_int,
    is_convertible_to_float,
)


__all__ = [
    "IsConvertibleToIntAction",
    "IsConvertibleToFloatAction",
    "IsTruthyAction",
    "IsFalsyAction",
]


class IsConvertibleToIntAction(Action):
    """Check if value can be convertible to int"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check if all values in list are convertible to int
            if False in [is_convertible_to_int(value) for value in values]:
                raise ValueError(
                    "at least one value cannot be converted to int"
                )
        else:
            # Check if value is convertible to int
            value = values
            if not is_convertible_to_int(value):
                raise ValueError("value cannot be converted to int")

        setattr(namespace, self.dest, values)


class IsConvertibleToFloatAction(Action):
    """asd asda sd"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check if all values in list are convertible to float
            if False in [is_convertible_to_float(value) for value in values]:
                raise ValueError(
                    "at least one value cannot be converted to float"
                )
        else:
            # Check if value is convertible to float
            value = values
            if not is_convertible_to_float(value):
                raise ValueError("value cannot be converted to float")

        setattr(namespace, self.dest, values)
