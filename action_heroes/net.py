from argparse import Action
from action_heroes.utils import CheckAction

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


class IPIsValidIPv4AddressAction(CheckAction):
    """Check if ip address is valid ipv4 address"""

    func = is_valid_ipv4_address
    err_msg_singular = "Atleast one ip address is an invalid ipv4 address"
    err_msg_plural = "ip address is invalid ipv4 address"


class IPIsValidIPv6AddressAction(CheckAction):
    """Check if ip address is valid ipv6 address"""

    func = is_valid_ipv6_address
    err_msg_singular = "Atleast one ip address is an invalid ipv6 address"
    err_msg_plural = "ip address is invalid ipv6 address"


class IPIsValidIPAddressAction(CheckAction):
    """Check if ip is valid ipv4 or ipv6 address"""

    func = is_valid_ip_address
    err_msg_singular = "Atleast one ip address is an invalid ipv(4/6) address"
    err_msg_plural = "ip address is invalid ip address"


class URLIsReachableAction(CheckAction):
    """Check if URL is reachable"""

    func = is_reachable_url
    err_msg_singular = "Atleast one URL is not reachable"
    err_msg_plural = "URL is not reachable"


class URLIsNotReachableAction(CheckAction):
    """Check if URL is not reachable"""

    def func(value):
        return not is_reachable_url(value)

    err_msg_singular = "Atleast one URL is not reachable"
    err_msg_plural = "URL is not reachable"


class URLWithHTTPResponseStatusCodeAction(Action):
    """Check if upplied URL responds with expected HTTP response status code

    Params:
        Expected HTTP Response Status Code

    """

    def __call__(self):
        raise NotImplementedError
