from action_hero.net import (
    IPIsValidIPAddressAction,
    IPIsValidIPv4AddressAction,
    IPIsValidIPv6AddressAction,
    URLWithHTTPResponseStatusCodeAction,
    URLIsNotReachableAction,
    URLIsReachableAction,
)

from action_hero.utils import (
    ActionHeroTestCase,
    run_only_when_when_internet_is_up,
)


class TestIPIsValidIPv4AddressAction(ActionHeroTestCase):
    def test_on_valid_ipv4_address(self):
        self.parser.add_argument("--ip", action=IPIsValidIPv4AddressAction)
        # Parse without raising any errors
        self.parser.parse_args(["--ip", "192.168.0.2"])

    def test_on_invalid_ipv4_address(self):
        self.parser.add_argument("--ip", action=IPIsValidIPv4AddressAction)
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
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", *ips])

    def test_on_mixed_valid_and_invalid_ipv4_addresses_list(self):
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPv4AddressAction
        )
        valid = ["192.168.0.2"]
        invalid = ["500.168.0.1"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", *valid, *invalid])


class TestIPIsValidIPV6Action(ActionHeroTestCase):
    def test_on_valid_ipv6_address(self):
        self.parser.add_argument("--ip", action=IPIsValidIPv6AddressAction)
        # Parse without raising any errors
        self.parser.parse_args(["--ip", "FE80::0202:B3FF:FE1E:8329"])

    def test_on_invalid_ipv6_address(self):
        self.parser.add_argument("--ip", action=IPIsValidIPv6AddressAction)
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
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", *ips])

    def test_on_mixed_valid_and_invalid_ipv6_addresses_list(self):
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPv6AddressAction
        )
        valid = ["192.168.0.2"]
        invalid = ["122.168.0.1", "0.0.0.0"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", *valid, *invalid])


class TestIPIsValidIPAddressAction(ActionHeroTestCase):
    def test_on_valid_ipv4_address(self):
        self.parser.add_argument("--ip", action=IPIsValidIPAddressAction)
        # Parse without raising any errors
        self.parser.parse_args(["--ip", "192.168.0.2"])

    def test_on_invalid_ipv4_address(self):
        self.parser.add_argument("--ip", action=IPIsValidIPAddressAction)
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", "500.168.0.1"])

    def test_on_valid_ipv4_address_list(self):
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPAddressAction
        )
        ips = ["192.168.0.2"]
        # Parse without raising any errors
        self.parser.parse_args(["--ip", *ips])

    def test_on_invalid_ipv4_address_list(self):
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPAddressAction
        )
        ips = ["500.168.0.1", "2001:db8:0:1"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", *ips])

    def test_on_mixed_valid_and_invalid_ipv4_addresses_list(self):
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPAddressAction
        )
        valid = ["192.168.0.2"]
        invalid = ["500.168.0.1"]
        # Asser error raised on parse
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", *valid, *invalid])

    def test_on_valid_ipv6_address(self):
        self.parser.add_argument("--ip", action=IPIsValidIPAddressAction)
        # Parse without raising any errors
        self.parser.parse_args(["--ip", "FE80::0202:B3FF:FE1E:8329"])

    def test_on_invalid_ipv6_address(self):
        self.parser.add_argument("--ip", action=IPIsValidIPAddressAction)
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", "1000.168.0.1"])

    def test_on_valid_ipv6_address_list(self):
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPAddressAction
        )
        ips = ["2001:db8:1::ab9:C0A8:102", "FE80::0202:B3FF:FE1E:8329"]
        # Parse without raising any errors
        self.parser.parse_args(["--ip", *ips])

    def test_on_invalid_ipv6_address_list(self):
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPAddressAction
        )
        ips = [":AA:2001:db8:1::ab9:C0A8:102", ":::FE80::02:B3:FE1E:8329"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", *ips])

    def test_on_mixed_valid_and_invalid_ipv4_and_ipv6_addresses_list(self):
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPAddressAction
        )
        valid = ["192.168.0.2"]
        invalid = ["x122.168.0.1", "0.0.0.0.0.0"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", *valid, *invalid])

    def test_on_mixed_valid_ipv4_and_ipv6_addresses_list(self):
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPAddressAction
        )
        ips = [
            # "FE80::0202:B3FF:FE1E:8329",
            "192.168.0.2",
            "20.0.0.120",
        ]
        # Parse without raising any errors
        self.parser.parse_args(["--ip", *ips])

    def test_on_mixed_invalid_ipv4_and_ipv6_addresses_list(self):
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPAddressAction
        )
        invalid = [
            "a.168.0.2",
            "120",
            ":AA:2001:db8:1::ab9:C0A8:102",
            ":::FE80::02:B3:FE1E:8329",
        ]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", *invalid])


class TestURLIsReachableAction(ActionHeroTestCase):
    @run_only_when_when_internet_is_up(urls=["http://www.google.com"])
    def test_on_reachable_url(self):
        self.parser.add_argument("--url", action=URLIsReachableAction)
        url = "http://google.com"
        self.parser.parse_args(["--url", url])

    @run_only_when_when_internet_is_up(
        urls=["http://www.google.com", "http://www.microsoft.com"]
    )
    def test_on_reachable_urls(self):
        self.parser.add_argument(
            "--url", nargs="+", action=URLIsReachableAction
        )
        urls = ["http://www.google.com", "http://www.microsoft.com"]
        self.parser.parse_args(["--url", *urls])

    @run_only_when_when_internet_is_up(urls=["http://www.google.com"])
    def test_on_unreachable_url(self):
        self.parser.add_argument("--url", action=URLIsReachableAction)
        unreachable = "AAA"
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--url", unreachable])

    @run_only_when_when_internet_is_up(urls=["http://www.google.com"])
    def test_on_unreachable_urls(self):
        self.parser.add_argument(
            "--url", nargs="+", action=URLIsReachableAction
        )
        unreachable = ["AAA", "httt://www.notreal.com"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--url", *unreachable])


class TestURLIsNotReachableAction(ActionHeroTestCase):
    @run_only_when_when_internet_is_up(urls=["http://www.google.com"])
    def test_on_reachable_url(self):
        self.parser.add_argument("--url", action=URLIsNotReachableAction)
        url = "http://google.com"
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--url", url])

    @run_only_when_when_internet_is_up(
        urls=["http://www.google.com", "http://www.microsoft.com"]
    )
    def test_on_reachable_urls(self):
        self.parser.add_argument(
            "--url", nargs="+", action=URLIsNotReachableAction
        )
        urls = ["http://www.google.com", "http://www.microsoft.com"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--url", *urls])

    @run_only_when_when_internet_is_up(urls=["http://www.google.com"])
    def test_on_unreachable_url(self):
        self.parser.add_argument("--url", action=URLIsNotReachableAction)
        unreachable = "AAA"
        self.parser.parse_args(["--url", unreachable])

    @run_only_when_when_internet_is_up(urls=["http://www.google.com"])
    def test_on_unreachable_urls(self):
        self.parser.add_argument(
            "--url", nargs="+", action=URLIsNotReachableAction
        )
        unreachable = ["AAA", "YYY"]
        self.parser.parse_args(["--url", *unreachable])


class TestURLWithHTTPResponseStatusCodeAction(ActionHeroTestCase):
    @run_only_when_when_internet_is_up(urls=["http://www.google.com"])
    def test_on_reachable_url(self):
        self.parser.add_argument(
            "--url",
            action=URLWithHTTPResponseStatusCodeAction,
            # Request success codes 2xx
            action_values=["200", "201", "202", "203", "204"],
        )
        url = "http://google.com"
        self.parser.parse_args(["--url", url])

    def test_on_unreachable_url(self):
        self.parser.add_argument(
            "--url",
            action=URLWithHTTPResponseStatusCodeAction,
            # Request failure codes 4xx, 5xx
            action_values=[
                "400",
                "401",
                "402",
                "403",
                "404",
                "500",
                "501",
                "502",
                "503",
            ],
        )
        unreachable = "AAA"
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--url", unreachable])
