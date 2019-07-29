from argparse import Action

from action_heroes.types_utils import (
    is_convertible_to_int,
    is_convertible_to_float,
    is_convertible_to_UUID,
    is_truthy,
)


__all__ = [
    "IsConvertibleToIntAction",
    "IsConvertibleToFloatAction",
    "IsTruthyAction",
    "IsFalsyAction",
    "IsConvertibleToUUIDAction",
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


class IsTruthyAction(Action):
    """Checks if value is truthy"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check if all values in list are truthy
            if False in [is_truthy(value) for value in values]:
                raise ValueError(
                    "at least one value is falsey"
                )
        else:
            # Check if value is convertible to truthy
            value = values
            if not is_truthy(value):
                raise ValueError("value is not falsy")

        setattr(namespace, self.dest, values)


class IsFalsyAction(Action):
    """Checks if value is falsy"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check if all values in list are falsy
            if True in [is_truthy(value) for value in values]:
                raise ValueError(
                    "at least one value is truthy"
                )
        else:
            # Check if value is falsy
            value = values
            if is_truthy(value):
                raise ValueError("value is truthy")

        setattr(namespace, self.dest, values)


class IsConvertibleToUUIDAction(Action):
    """Checks if value is convertible to UUID"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check if all values in list are convertible to UUIDs
            if False in [is_convertible_to_UUID(value) for value in values]:
                raise ValueError(
                    "at least one value is not convertible to UUIDs"
                )
        else:
            # Check if value is convertible to UUIDs
            value = values
            if not is_convertible_to_UUID(value):
                raise ValueError("value is convertible to UUIDs")

        setattr(namespace, self.dest, values)
