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
    """Returns True if value is truthy

    Only attempting truthy when is string of zeroes 0/0.0

    Args:
        value (str): Value to check truthy for.

    Returns:
        bool: True if deemed truthy else False
    """
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

    UUID v.4 General Format:
      - xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx
      - where x is a hex digit and y is one of (8, 9, A, B)

    Using python uuid.UUID and as so,
    Supporting these forms:
      ca761232ed4211cebacd00aa0057b223
      CA761232-ED42-11CE-BACD-00AA0057B223
      {CA761232-ED42-11CE-BACD-00AA0057B223}
    Not supporting these forms
      (CA761232-ED42-11CE-BACD-00AA0057B223)
      {0xCA761232, 0xED42, 0x11CE, {0xBA, 0xCD, 0x00, 0xAA, *LINER BREAK*
      0x00, 0x57, 0xB2, 0x23}}

    Args:
        value (str): Value to attempt to convert to an UUID
        version (int): UUID version. Default is UUIDv4

    Returns:
        bool: True if deemed valid UUID

    """
    try:
        # 1. Check if can be converted to a UUID
        uuid.UUID(value, version=version)

    except (ValueError, AttributeError):
        # 2. Return false if cannot be converted to UUID
        return False

    else:
        # 3. Return true if can be converted to UUID
        return True
