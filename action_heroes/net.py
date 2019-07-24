import argparse


class ValidIPv4Action(argparse.Action):
    """Check if IP is valid ipv4 address"""
    pass


class ValidIPv6Action(argparse.Action):
    """Check if IP is valid ipv6 address"""
    pass


class ValidURLAction(argparse.Action):
    """Check if URL is valid"""
    pass


class ReachableURLAction(argparse.Action):
    """Check if URL is reachable"""
    pass


class URLWithHTTPResponseStatusCodeAction(argparse.Action):
    """Check is upplied URL responds with expected HTTP response status code

    Params:
        Expected HTTP Response Status Code

    """
    pass
