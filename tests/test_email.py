from action_hero.email import EmailIsValidAction
from action_hero.utils import ActionHeroTestCase


class TestEmailIsValidAction(ActionHeroTestCase):
    def test_on_valid_email(self):
        self.parser.add_argument("--email", action=EmailIsValidAction)
        email = "hello@service.com"
        # Parse without raising any errors
        self.parser.parse_args(["--email", email])

    def test_on_valid_emails_list(self):
        self.parser.add_argument(
            "--email", nargs="+", action=EmailIsValidAction
        )
        emails = ["hello@service.co.uk", "shawn@psych.com", "gus@psych.com"]
        # Parse without raising any errors
        self.parser.parse_args(["--email", *emails])

    def test_on_invalid_email(self):
        self.parser.add_argument("--email", action=EmailIsValidAction)
        email = "ampersand"
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--email", email])

    def test_on_invalid_emails_list(self):
        self.parser.add_argument(
            "--email", nargs="+", action=EmailIsValidAction
        )
        emails = ["friday", "person aol.com", "oopsemail"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--email", *emails])

    def test_on_mixed_valid_and_invalid_email_lists(self):
        self.parser.add_argument(
            "--email", nargs="+", action=EmailIsValidAction
        )
        emails = [
            "hello@service.co.uk",
            "shawn@psych.com",
            "gus@psych.com",
            "friday",
            "person aol.com",
            "oopsemail",
        ]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--email", *emails])
