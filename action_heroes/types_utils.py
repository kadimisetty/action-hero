__all__ = ["is_convertible_to_int", "is_convertible_to_float"]


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
