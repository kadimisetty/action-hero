import uuid


__all__ = [
    "is_convertible_to_UUID",
    "is_convertible_to_float",
    "is_convertible_to_int",
    "is_truthy",
]


def is_convertible_to_int(value):
    """Returns True if value is convertible to int"""
    try:
        int(value)
    except ValueError:
        return False
    else:
        return True


def is_convertible_to_float(value):
    """Returns True if value is convertible to float"""
    try:
        float(value)
    except ValueError:
        return False
    else:
        return True


def is_truthy(value):
    """Returns True if value is truthy"""
    try:
        # 1. Check if can be converted to a float
        float(value)

    except ValueError:
        # 2. Return truthy of value if cannot be converted to float
        return bool(value)

    else:
        # 3. Return truthy of value if can be converted to a float
        return bool(float(value))


def is_convertible_to_UUID(value, version=4):
    """Returns True if value is convertible to UUIDs

    Note:
        - UUID v.4
        - Format: xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx where
        - x is a hex digit and y is one of (8, 9, A, B)

    """
    try:
        # 1. Check if can be converted to a UUID
        uuid.UUID(value, version=version)

    except ValueError:
        # 2. Return false if cannot be converted to UUID
        return False

    else:
        # 3. Return true if can be converted to UUID
        return True
