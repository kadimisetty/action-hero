import ipaddress

import requests

__all__ = [
    "is_reachable_url",
    "is_valid_ip_address",
    "is_valid_ipv4_address",
    "is_valid_ipv6_address",
    "status_code_from_response_to_request_url",
]


def is_valid_ipv4_address(ip):
    """Return True if valid ipv4 address """

    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False


def is_valid_ipv6_address(ip):
    """Return True if valid ipv6 address """

    try:
        ipaddress.IPv6Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False


def is_valid_ip_address(ip):
    """Return True if valid ipv4 or ipv6 address """
    return is_valid_ipv4_address(ip) or is_valid_ipv6_address(ip)


def is_reachable_url(url):
    """Return True if url is reachable"""

    try:
        # raise_for_status() raises an exception on fail, else None
        requests.get(url).raise_for_status()
        return True

    except requests.exceptions.RequestException:
        return False


def status_code_from_response_to_request_url(url):
    """Return status code from response to request url"""

    try:
        return str(requests.get(url).status_code)

    except requests.exceptions.RequestException:
        return None
