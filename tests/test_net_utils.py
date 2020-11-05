import unittest

import requests

from action_hero.utils import run_only_when_when_internet_is_up
from action_hero.net_utils import (
    is_valid_ip_address,
    is_valid_ipv4_address,
    is_valid_ipv6_address,
    is_reachable_url,
    status_code_from_response_to_request_url,
    is_valid_email,
)


class TestIsEmailValid(unittest.TestCase):
    def test_on_valid_email(self):
        """
        Test if email is valid.

        Args:
            self: (todo): write your description
        """
        emails = ["hello@domain.com", "jobs@mac.com", "contact3@example.com"]
        [self.assertTrue(is_valid_email(email)) for email in emails]

    def test_on_invalid_email(self):
        """
        Test if the email addresses.

        Args:
            self: (todo): write your description
        """
        emails = ["hello", "downcase", "2"]
        [self.assertFalse(is_valid_email(email)) for email in emails]


class TestIsValidIPv4Address(unittest.TestCase):
    def test_on_valid_ipv6_address_string(self):
        """
        Test if ipv6 address.

        Args:
            self: (todo): write your description
        """
        self.assertFalse(is_valid_ipv4_address("2001:db8::1000"))

    def test_on_valid_ipv4_address_string(self):
        """
        Configure the ipv4 address is valid.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(is_valid_ipv4_address("192.168.0.1"))

    def test_on_invalid_ipv4_address_string(self):
        """
        This method for ipv4 address.

        Args:
            self: (todo): write your description
        """
        self.assertFalse(is_valid_ipv4_address("500.168.0.1"))

    def test_on_valid_ipv4_address_numbers(self):
        """
        Test if the given ipv4 address is valid.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(is_valid_ipv4_address(3232235521))

    def test_on_invalid_ipv4_address_numbers(self):
        """
        !

        Args:
            self: (todo): write your description
        """
        self.assertFalse(is_valid_ipv4_address(8000000000))

    def test_on_valid_ipv4_address_bytes(self):
        """
        Test if the ipv4 address.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(is_valid_ipv4_address(b"\xC0\xA8\x00\x01"))

    def test_on_invalid_ipv4_address_bytes(self):
        """
        Test if the ipv4 address is valid.

        Args:
            self: (todo): write your description
        """
        self.assertFalse(is_valid_ipv4_address(b"\xC0\xA8\x00"))


class TestIsValidIPv6Address(unittest.TestCase):
    def test_on_valid_ipv4_address_string(self):
        """
        The valid ipv4 ipv6 address.

        Args:
            self: (todo): write your description
        """
        self.assertFalse(is_valid_ipv6_address("192.168.0.1"))

    def test_on_valid_ipv6_address_string(self):
        """
        Configure ipv6 address is valid.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(is_valid_ipv6_address("2001:db8::1000"))

    def test_on_invalid_ipv6_address_string(self):
        """
        Configure the ipv6 address.

        Args:
            self: (todo): write your description
        """
        self.assertFalse(is_valid_ipv6_address("192.168.0.1"))

    def test_on_compressed_valid_ipv6_address_string(self):
        """
        Configure the ipv6 ipv6 ipv6 address.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(is_valid_ipv6_address("::1:1:1"))


class TestIsValidIPAddress(unittest.TestCase):
    def test_on_valid_ipv4_address_string(self):
        """
        Test if ipv4 ipv4 address.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(is_valid_ip_address("192.168.0.1"))

    def test_on_valid_ipv6_address_string(self):
        """
        Configure ipv6 address is valid.

        Args:
            self: (todo): write your description
        """
        self.assertTrue(is_valid_ip_address("2001:db8::1000"))

    def test_on_invalid_ipv6_address_string(self):
        """
        Configure ipv6 address is valid.

        Args:
            self: (todo): write your description
        """
        self.assertFalse(is_valid_ip_address("192.168.0.x"))

    def test_on_invalid_ipv4_address_bytes(self):
        """
        Test if the ipv4 address is valid.

        Args:
            self: (todo): write your description
        """
        self.assertFalse(is_valid_ip_address(b"\xC0\xA8\x00"))


class TestIsURLReachable(unittest.TestCase):
    @run_only_when_when_internet_is_up
    def test_on_reachable_url(self):
        """
        Test if the url1 and url1.

        Args:
            self: (todo): write your description
        """
        url1 = "http://www.google.com"
        self.assertTrue(is_reachable_url(url1))

    def test_on_unreachable_url(self):
        """
        Test whether the url1 url1.

        Args:
            self: (todo): write your description
        """
        url1 = "madeupurl.example.xyz"
        self.assertFalse(is_reachable_url(url1))


class TestStatusCodeFromResponseToRequestURL(unittest.TestCase):
    @run_only_when_when_internet_is_up
    def test_on_reachable_url(self):
        """
        Test if the http post request.

        Args:
            self: (todo): write your description
        """
        try:
            url1 = "http://www.google.com"
            response = requests.get(url1)  # Raises RequestException on fail
            self.assertEqual(
                status_code_from_response_to_request_url(url1),  # None on fail
                response.status_code,
            )

        # Do nothing on response error
        except requests.exceptions.RequestException:
            pass

    def test_on_unreahable_url(self):
        """
        Test if http post request is test.

        Args:
            self: (todo): write your description
        """
        try:
            url1 = "madeupurl.example.xyz"
            response = requests.get(url1)  # Raises RequestException on fail
            self.assertEqual(
                status_code_from_response_to_request_url(url1),  # None on fail
                response.status_code,
            )

        # Do nothing on response error
        except requests.exceptions.RequestException:
            pass

    def test_on_malformed_url_returns_none_on_request_failure(self):
        """
        Test if the response was received. org.

        Args:
            self: (todo): write your description
        """
        url1 = "AAA"
        self.assertIsNone(status_code_from_response_to_request_url(url1))
