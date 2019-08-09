from action_hero.email_utils import is_valid_email
from action_hero.utils import CheckAction


__all__ = ["EmailIsValidAction"]


class EmailIsValidAction(CheckAction):
    """Check if email address is valid"""

    func = is_valid_email
    error_message = "Invalid email address(es)"
