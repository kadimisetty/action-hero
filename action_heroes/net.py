from argparse import Action

from action_heroes.net_utils import (
    is_valid_ip_address,
    is_valid_ipv4_address,
    is_valid_ipv6_address,
    is_reachable_url,
    status_code_from_response_to_request_url,
)


class IPIsValidIPv4AddressAction(Action):
    """Check if IP is valid ipv4 address"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check list of ips are all valid ipv4 addresses
            if False in [is_valid_ipv4_address(path) for path in values]:
                raise ValueError(
                    "ips has atleast one ip that is not a valid ipv4 address"
                )
        else:
            # Check ip is valid ip4 address
            path = values
            if not is_valid_ipv4_address(path):
                raise ValueError("ip is not a valid ipv4 address")

        setattr(namespace, self.dest, values)


class IPIsValidIPv6AddressAction(Action):
    """Check if IP is valid ipv6 address"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check list of ips are all valid ipv6 addresses
            if False in [is_valid_ipv6_address(path) for path in values]:
                raise ValueError(
                    "ips has atleast one ip that is not a valid ipv6 address"
                )
        else:
            # Check ip is valid ip6 address
            path = values
            if not is_valid_ipv6_address(path):
                raise ValueError("ip is not a valid ipv6 address")

        setattr(namespace, self.dest, values)


class IPIsValidIPAddressAction(Action):
    """Check if ip is valid ipv4 or ipv6 address"""

    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, list):
            # Check list of ips are all valid ipv4/ipv6 addresses
            if False in [is_valid_ipv6_address(path) for path in values]:
                raise ValueError(
                    "ips has atleast one ip that is not a valid ip address"
                )
        else:
            # Check ip is valid ipv4/ipv6 address
            path = values
            if not is_valid_ipv6_address(path):
                raise ValueError("ip is not a valid ip address")

        setattr(namespace, self.dest, values)


class URLIsReachableAction(Action):
    """Check if URL is reachable"""

    def __call__(self):
        raise NotImplementedError


class URLIsNotReachableAction(Action):
    """Check if URL is reachable"""

    def __call__(self):
        raise NotImplementedError


class URLWithHTTPResponseStatusCodeAction(Action):
    """Check if upplied URL responds with expected HTTP response status code

    Params:
        Expected HTTP Response Status Code

    """

    def __call__(self):
        raise NotImplementedError
