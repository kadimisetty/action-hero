from argparse import Action

from action_heroes.net_utils import (
    is_valid_ip_address,
    is_valid_ipv4_address,
    is_valid_ipv6_address,
    is_reachable_url,
)


__all__ = [
    "IPIsValidIPAddressAction",
    "IPIsValidIPAddressAction",
    "IPIsValidIPv4AddressAction",
    "IPIsValidIPv6AddressAction",
    "URLIsNotReachableAction",
    "URLIsReachableAction",
    "URLWithHTTPResponseStatusCodeAction",
]


class IPIsValidIPv4AddressAction(Action):
    """Check if IP is valid ipv4 address"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check list of ips are all valid ipv4 addresses
            if False in [is_valid_ipv4_address(ip) for ip in values]:
                raise ValueError(
                    "ips has atleast one ip that is not a valid ipv4 address"
                )
        else:
            # Check ip is valid ip4 address
            ip = values
            if not is_valid_ipv4_address(ip):
                raise ValueError("ip is not a valid ipv4 address")

        setattr(namespace, self.dest, values)


class IPIsValidIPv6AddressAction(Action):
    """Check if IP is valid ipv6 address"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check list of ips are all valid ipv6 addresses
            if False in [is_valid_ipv6_address(ip) for ip in values]:
                raise ValueError(
                    "ips has atleast one ip that is not a valid ipv6 address"
                )
        else:
            # Check ip is valid ip6 address
            ip = values
            if not is_valid_ipv6_address(ip):
                raise ValueError("ip is not a valid ipv6 address")

        setattr(namespace, self.dest, values)


class IPIsValidIPAddressAction(Action):
    """Check if ip is valid ipv4 or ipv6 address"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check list of ip are all valid ip addresses
            if False in [is_valid_ip_address(ip) for ip in values]:
                raise ValueError(
                    "ips has atleast one ip that is not a valid ipv6 address"
                )
        else:
            # Check ip is valid ip address
            ip = values
            if not is_valid_ip_address(ip):
                raise ValueError("ip is not a valid ipv6 address")

        setattr(namespace, self.dest, values)


class URLIsReachableAction(Action):
    """Check if URL is reachable"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check list of urls are all reachable
            if False in [is_reachable_url(url) for url in values]:
                raise ValueError(
                    "urls has atleast one url that is not reachable"
                )
        else:
            # Check url is reachable
            url = values
            if not is_reachable_url(url):
                raise ValueError("url is not reachable")

        setattr(namespace, self.dest, values)


class URLIsNotReachableAction(Action):
    """Check if URL is not reachable"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check list of urls are all not reachable
            if True in [is_reachable_url(url) for url in values]:
                raise ValueError(
                    "urls has atleast one url that is reachable"
                )
        else:
            # Check url is not reachable
            url = values
            if is_reachable_url(url):
                raise ValueError("url is reachable")

        setattr(namespace, self.dest, values)


class URLWithHTTPResponseStatusCodeAction(Action):
    """Check if upplied URL responds with expected HTTP response status code

    Params:
        Expected HTTP Response Status Code

    """
    def __call__(self):
        raise NotImplementedError
