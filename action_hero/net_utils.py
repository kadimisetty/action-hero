import ipaddress
import re

import requests

__all__ = [
    "is_reachable_url",
    "is_valid_email",
    "is_valid_ip_address",
    "is_valid_ipv4_address",
    "is_valid_ipv6_address",
    "status_code_from_response_to_request_url",
]


def is_valid_email(email):
    """Return True if email is valid

    There is no perfect regex match for email.
    Using the email regex pattern from http://emailregex.com

    Args:
        email (str): The email address to check validity for
    """
    pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    return bool(pattern.match(email))


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
