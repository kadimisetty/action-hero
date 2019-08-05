from action_hero.utils import CheckAction, CheckPresentInValuesAction

from action_hero.net_utils import (
    status_code_from_response_to_request_url,
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
    err_msg_singular = "ip address is invalid ipv4 address"
    err_msg_plural = "Atleast one ip address is an invalid ipv4 address"


class IPIsValidIPv6AddressAction(CheckAction):
    """Check if ip address is valid ipv6 address"""

    func = is_valid_ipv6_address
    err_msg_singular = "ip address is invalid ipv6 address"
    err_msg_plural = "Atleast one ip address is an invalid ipv6 address"


class IPIsValidIPAddressAction(CheckAction):
    """Check if ip is valid ipv4 or ipv6 address"""

    func = is_valid_ip_address
    err_msg_singular = "ip address is invalid ip address"
    err_msg_plural = "Atleast one ip address is an invalid ipv(4/6) address"


class URLIsReachableAction(CheckAction):
    """Check if URL is reachable"""

    func = is_reachable_url
    err_msg_singular = "URL is not reachable"
    err_msg_plural = "Atleast one URL is not reachable"


class URLIsNotReachableAction(CheckAction):
    """Check if URL is not reachable"""

    def func(value):
        return not is_reachable_url(value)

    err_msg_singular = "URL is not reachable"
    err_msg_plural = "Atleast one URL is not reachable"


class URLWithHTTPResponseStatusCodeAction(CheckPresentInValuesAction):
    """Check if supplied URL responds with status code in action_values"""

    func = status_code_from_response_to_request_url
    err_msg_singular = "Response from URL does not have expected status code."
    err_msg_plural = (
        "Response from at least one URL does not have expected status code."
    )
