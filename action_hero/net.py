from action_hero.utils import CheckAction, CheckPresentInValuesAction

from action_hero.net_utils import (
    is_reachable_url,
    is_valid_ip_address,
    is_valid_ipv4_address,
    is_valid_ipv6_address,
    status_code_from_response_to_request_url,
    is_valid_email,
)


__all__ = [
    "EmailIsValidAction",
    "IPIsValidIPAddressAction",
    "IPIsValidIPv4AddressAction",
    "IPIsValidIPv6AddressAction",
    "URLIsNotReachableAction",
    "URLIsReachableAction",
    "URLWithHTTPResponseStatusCodeAction",
]


class EmailIsValidAction(CheckAction):
    """Check if email address is valid"""

    func = is_valid_email
    error_message = "Invalid email address(es)"


class IPIsValidIPv4AddressAction(CheckAction):
    """Check if ip address is valid ipv4 address"""

    func = is_valid_ipv4_address
    error_message = "Invalid ipv4 address(es)"


class IPIsValidIPv6AddressAction(CheckAction):
    """Check if ip address is valid ipv6 address"""

    func = is_valid_ipv6_address
    error_message = "Invalid ipv6 address(es)"


class IPIsValidIPAddressAction(CheckAction):
    """Check if ip is valid ipv4 or ipv6 address"""

    func = is_valid_ip_address
    error_message = "Invalid ip address(es)"


class URLIsReachableAction(CheckAction):
    """Check if URL is reachable"""

    func = is_reachable_url
    error_message = "Unreachable URL(s)"


class URLIsNotReachableAction(CheckAction):
    """Check if URL is not reachable"""

    def func(value):
        return not is_reachable_url(value)

    error_message = "Reachable URL(s)"


class URLWithHTTPResponseStatusCodeAction(CheckPresentInValuesAction):
    """Check if supplied URL responds with status code in action_values"""

    func = status_code_from_response_to_request_url
    error_message = "URL(s) with unexpected status codes"
