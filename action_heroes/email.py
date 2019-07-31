from action_heroes.email_utils import is_valid_email
from action_heroes.utils import CheckAction


__all__ = ["EmailIsValidAction"]


class EmailIsValidAction(CheckAction):
    """Checks if email address is valid"""

    func = is_valid_email
    err_msg_singular = "Atleast one supplied email address is invalid"
    err_msg_plural = "Email address is invalid"
