import unittest

from action_hero.email_utils import is_valid_email


class TestIsEmailValid(unittest.TestCase):
    def test_on_valid_email(self):
        emails = ["hello@domain.com", "jobs@mac.com", "contact3@example.com"]
        [self.assertTrue(is_valid_email(email)) for email in emails]

    def test_on_invalid_email(self):
        emails = ["hello", "downcase", "2"]
        [self.assertFalse(is_valid_email(email)) for email in emails]
