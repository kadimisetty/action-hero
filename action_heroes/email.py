from argparse import Action

from action_heroes.email_utils import is_valid_email


__all__ = [
    "EmailIsValidAction",
]


class EmailIsValidAction(Action):
    """Checks if email address is valid"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check list of emails are all valid email addresses
            if False in [is_valid_email(email) for email in values]:
                raise ValueError(
                    "emails has atleast one invalid email address"
                )
        else:
            # Check if email is valid email address
            email = values
            if not is_valid_email(email):
                raise ValueError("email address is invalid")

        setattr(namespace, self.dest, values)
