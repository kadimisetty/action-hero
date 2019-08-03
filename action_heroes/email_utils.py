import re


__all__ = [
    "is_valid_email",
]


def is_valid_email(email):
    """Returns True if email is valid

    There is no perfect regex match for email.
    Using the email regex pattern from http://emailregex.com

    Args:
        email (str): The email address to check validity for

    Returns:
        bool: True if deemed valid email address else False

    """
    pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    return True if pattern.match(email) else False
