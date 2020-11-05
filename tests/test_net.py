from action_hero import (
    IPIsValidIPAddressAction,
    IPIsValidIPv4AddressAction,
    IPIsValidIPv6AddressAction,
    URLIsNotReachableAction,
    URLIsReachableAction,
    URLWithHTTPResponseStatusCodeAction,
    EmailIsValidAction,
)

from action_hero.utils import (
    ActionHeroTestCase,
    run_only_when_when_internet_is_up,
)


class TestEmailIsValidAction(ActionHeroTestCase):
    def test_on_valid_email(self):
        """
        Test if the email.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--email", action=EmailIsValidAction)
        email = "hello@service.com"
        # Parse without raising any errors
        self.parser.parse_args(["--email", email])

    def test_on_valid_emails_list(self):
        """
        Test if the email addresses.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--email", nargs="+", action=EmailIsValidAction
        )
        emails = ["hello@service.co.uk", "shawn@psych.com", "gus@psych.com"]
        # Parse without raising any errors
        self.parser.parse_args(["--email", *emails])

    def test_on_invalid_email(self):
        """
        Test if the email is valid.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--email", action=EmailIsValidAction)
        email = "ampersand"
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--email", email])

    def test_on_invalid_emails_list(self):
        """
        Test if the emails are valid emails.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--email", nargs="+", action=EmailIsValidAction
        )
        emails = ["friday", "person aol.com", "oopsemail"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--email", *emails])

    def test_on_mixed_valid_and_invalid_email_lists(self):
        """
        Test if the emails that are valid.

        Args:
            self: (todo): write your description
        """
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


class TestIPIsValidIPv4AddressAction(ActionHeroTestCase):
    def test_on_valid_ipv4_address(self):
        """
        Test if the ipv4 address is valid.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--ip", action=IPIsValidIPv4AddressAction)
        # Parse without raising any errors
        self.parser.parse_args(["--ip", "192.168.0.2"])

    def test_on_invalid_ipv4_address(self):
        """
        Test if the ip address is valid.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--ip", action=IPIsValidIPv4AddressAction)
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", "500.168.0.1"])

    def test_on_valid_ipv4_address_list(self):
        """
        Test if ipv4 ip address.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPv4AddressAction
        )
        ips = ["192.168.0.2"]
        # Parse without raising any errors
        self.parser.parse_args(["--ip", *ips])

    def test_on_invalid_ipv4_address_list(self):
        """
        Test if ipv4 ipv4.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPv4AddressAction
        )
        ips = ["500.168.0.1", "2001:db8:0:1"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", *ips])

    def test_on_mixed_valid_and_invalid_ipv4_addresses_list(self):
        """
        Test on ipv4.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPv4AddressAction
        )
        valid = ["192.168.0.2"]
        invalid = ["500.168.0.1"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", *valid, *invalid])


class TestIPIsValidIPV6Action(ActionHeroTestCase):
    def test_on_valid_ipv6_address(self):
        """
        Test if the ipv6 address is valid.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--ip", action=IPIsValidIPv6AddressAction)
        # Parse without raising any errors
        self.parser.parse_args(["--ip", "FE80::0202:B3FF:FE1E:8329"])

    def test_on_invalid_ipv6_address(self):
        """
        Test if the ip address is valid.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--ip", action=IPIsValidIPv6AddressAction)
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", "10.168.0.1"])

    def test_on_valid_ipv6_address_list(self):
        """
        Test if ipv6 is valid.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPv6AddressAction
        )
        ips = ["2001:db8:1::ab9:C0A8:102", "FE80::0202:B3FF:FE1E:8329"]
        # Parse without raising any errors
        self.parser.parse_args(["--ip", *ips])

    def test_on_invalid_ipv6_address_list(self):
        """
        Test if ipv6 is valid.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPv6AddressAction
        )
        ips = ["122.168.0.1", "0.0.0.0"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", *ips])

    def test_on_mixed_valid_and_invalid_ipv6_addresses_list(self):
        """
        Test on on ip addresses are valid.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPv6AddressAction
        )
        valid = ["192.168.0.2"]
        invalid = ["122.168.0.1", "0.0.0.0"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", *valid, *invalid])


class TestIPIsValidIPAddressAction(ActionHeroTestCase):
    def test_on_valid_ipv4_address(self):
        """
        Test if the ipv4 address.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--ip", action=IPIsValidIPAddressAction)
        # Parse without raising any errors
        self.parser.parse_args(["--ip", "192.168.0.2"])

    def test_on_invalid_ipv4_address(self):
        """
        Test if the ip address is valid.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--ip", action=IPIsValidIPAddressAction)
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", "500.168.0.1"])

    def test_on_valid_ipv4_address_list(self):
        """
        Test if ipv4 ipv4 address.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPAddressAction
        )
        ips = ["192.168.0.2"]
        # Parse without raising any errors
        self.parser.parse_args(["--ip", *ips])

    def test_on_invalid_ipv4_address_list(self):
        """
        Test if ipv4 ipv4.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPAddressAction
        )
        ips = ["500.168.0.1", "2001:db8:0:1"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", *ips])

    def test_on_mixed_valid_and_invalid_ipv4_addresses_list(self):
        """
        Test on ipv4.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPAddressAction
        )
        valid = ["192.168.0.2"]
        invalid = ["500.168.0.1"]
        # Asser error raised on parse
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", *valid, *invalid])

    def test_on_valid_ipv6_address(self):
        """
        Test if the ipv6 address is valid.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--ip", action=IPIsValidIPAddressAction)
        # Parse without raising any errors
        self.parser.parse_args(["--ip", "FE80::0202:B3FF:FE1E:8329"])

    def test_on_invalid_ipv6_address(self):
        """
        Test if an interface.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--ip", action=IPIsValidIPAddressAction)
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", "1000.168.0.1"])

    def test_on_valid_ipv6_address_list(self):
        """
        Test if ipv6 is valid.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPAddressAction
        )
        ips = ["2001:db8:1::ab9:C0A8:102", "FE80::0202:B3FF:FE1E:8329"]
        # Parse without raising any errors
        self.parser.parse_args(["--ip", *ips])

    def test_on_invalid_ipv6_address_list(self):
        """
        Test if ipv6 is valid.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPAddressAction
        )
        ips = [":AA:2001:db8:1::ab9:C0A8:102", ":::FE80::02:B3:FE1E:8329"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", *ips])

    def test_on_mixed_valid_and_invalid_ipv4_and_ipv6_addresses_list(self):
        """
        Test on_on_validresses is valid.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--ip", nargs="+", action=IPIsValidIPAddressAction
        )
        valid = ["192.168.0.2"]
        invalid = ["x122.168.0.1", "0.0.0.0.0.0"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--ip", *valid, *invalid])

    def test_on_mixed_valid_ipv4_and_ipv6_addresses_list(self):
        """
        Test if ipv6 command.

        Args:
            self: (todo): write your description
        """
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
        """
        Test if the ipv6 command.

        Args:
            self: (todo): write your description
        """
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
        """
        Test if the test is received.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--url", action=URLIsReachableAction)
        url = "http://google.com"
        self.parser.parse_args(["--url", url])

    @run_only_when_when_internet_is_up(
        urls=["http://www.google.com", "http://www.microsoft.com"]
    )
    def test_on_reachable_urls(self):
        """
        Test if the relevant http query starts on_args.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--url", nargs="+", action=URLIsReachableAction
        )
        urls = ["http://www.google.com", "http://www.microsoft.com"]
        self.parser.parse_args(["--url", *urls])

    @run_only_when_when_internet_is_up(urls=["http://www.google.com"])
    def test_on_unreachable_url(self):
        """
        Test if_onable_url.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--url", action=URLIsReachableAction)
        unreachable = "AAA"
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--url", unreachable])

    @run_only_when_when_internet_is_up(urls=["http://www.google.com"])
    def test_on_unreachable_urls(self):
        """
        Test if the unreachable command.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--url", nargs="+", action=URLIsReachableAction
        )
        unreachable = ["AAA", "httt://www.notreal.com"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--url", *unreachable])


class TestURLIsNotReachableAction(ActionHeroTestCase):
    @run_only_when_when_internet_is_up(urls=["http://www.google.com"])
    def test_on_reachable_url(self):
        """
        Test if the received received from the database.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--url", action=URLIsNotReachableAction)
        url = "http://google.com"
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--url", url])

    @run_only_when_when_internet_is_up(
        urls=["http://www.google.com", "http://www.microsoft.com"]
    )
    def test_on_reachable_urls(self):
        """
        Test on on_onable on_url is enabled.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--url", nargs="+", action=URLIsNotReachableAction
        )
        urls = ["http://www.google.com", "http://www.microsoft.com"]
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--url", *urls])

    @run_only_when_when_internet_is_up(urls=["http://www.google.com"])
    def test_on_unreachable_url(self):
        """
        The unreachable test url.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument("--url", action=URLIsNotReachableAction)
        unreachable = "AAA"
        self.parser.parse_args(["--url", unreachable])

    @run_only_when_when_internet_is_up(urls=["http://www.google.com"])
    def test_on_unreachable_urls(self):
        """
        Test if the unreachable url.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--url", nargs="+", action=URLIsNotReachableAction
        )
        unreachable = ["AAA", "YYY"]
        self.parser.parse_args(["--url", *unreachable])


class TestURLWithHTTPResponseStatusCodeAction(ActionHeroTestCase):
    @run_only_when_when_internet_is_up(urls=["http://www.google.com"])
    def test_on_reachable_url(self):
        """
        Test if we needable query.

        Args:
            self: (todo): write your description
        """
        self.parser.add_argument(
            "--url",
            action=URLWithHTTPResponseStatusCodeAction,
            # Request success codes 2xx
            action_values=["200", "201", "202", "203", "204"],
        )
        url = "http://google.com"
        self.parser.parse_args(["--url", url])

    def test_on_unreachable_url(self):
        """
        The unreachable test url.

        Args:
            self: (todo): write your description
        """
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
