import re


__all__ = [
    "is_valid_email",
]


def is_valid_email(email):
    """Returns True if email is valid

    Note:
        There is no perfect regex match for email.
        Using the email regex pattern from http://emailregex.com
    """
    pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    return True if pattern.match(email) else False
