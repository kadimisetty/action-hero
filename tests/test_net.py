import unittest
from argparse import ArgumentParser

from action_heroes.net import (
    IPIsValidIPv4AddressAction,
    IPIsValidIPv6AddressAction,
    IPIsValidIPAddressAction,
)

from action_heroes.net_utils import (
    is_valid_ip_address,
    is_valid_ipv4_address,
    is_valid_ipv6_address,
    is_reachable_url,
    status_code_from_response_to_request_url,
)


class ParserEnclosedTestCase(unittest.TestCase):
    def setUp(self):
        """Setup new parser"""
        self.parser = ArgumentParser()


class TestIPIsValidIPv4AddressAction(ParserEnclosedTestCase):
    def test_on_valid_ipv4_address(self):
        self.parser.add_argument("--ip", action=IPIsValidIPv4AddressAction)
        # Parse without raising any errors
        self.parser.parse_args(["--ip", "192.168.0.2"])

    def test_on_invalid_ipv4_address(self):
        self.parser.add_argument("--ip", action=IPIsValidIPv4AddressAction)
        # Asser error raised on parse
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", "500.168.0.1"])

    def test_on_valid_ipv4_address_list(self):
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPv4AddressAction
        )
        ips = ["192.168.0.2"]
        # Parse without raising any errors
        self.parser.parse_args(["--ip", *ips])

    def test_on_invalid_ipv4_address_list(self):
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPv4AddressAction
        )
        ips = ["500.168.0.1", "2001:db8:0:1"]
        # Asser error raised on parse
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", *ips])

    def test_on_mixed_valid_and_invalid_ipv4_addresses_list(self):
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPv4AddressAction
        )
        valid = ["192.168.0.2"]
        invalid = ["500.168.0.1"]
        # Asser error raised on parse
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", *valid, *invalid])


class TestIPIsValidIPV6Action(ParserEnclosedTestCase):
    def test_on_valid_ipv6_address(self):
        self.parser.add_argument("--ip", action=IPIsValidIPv6AddressAction)
        # Parse without raising any errors
        self.parser.parse_args(["--ip", "FE80::0202:B3FF:FE1E:8329"])

    def test_on_invalid_ipv6_address(self):
        self.parser.add_argument("--ip", action=IPIsValidIPv6AddressAction)
        # Asser error raised on parse
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", "10.168.0.1"])

    def test_on_valid_ipv6_address_list(self):
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPv6AddressAction
        )
        ips = ["2001:db8:1::ab9:C0A8:102", "FE80::0202:B3FF:FE1E:8329"]
        # Parse without raising any errors
        self.parser.parse_args(["--ip", *ips])

    def test_on_invalid_ipv6_address_list(self):
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPv6AddressAction
        )
        ips = ["122.168.0.1", "0.0.0.0"]
        # Asser error raised on parse
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", *ips])

    def test_on_mixed_valid_and_invalid_ipv6_addresses_list(self):
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPv6AddressAction
        )
        valid = ["192.168.0.2"]
        invalid = ["122.168.0.1", "0.0.0.0"]
        # Asser error raised on parse
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", *valid, *invalid])


class TestIPIsValidIPAction(ParserEnclosedTestCase):
    pass
