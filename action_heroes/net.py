from argparse import Action


class IPIsValidIPv4AddressAction(Action):
    """Check if IP is valid ipv4 address"""
    pass


class IPIsValidIPV6Action(Action):
    """Check if IP is valid ipv6 address"""
    pass


class URLIsValidAction(Action):
    """Check if URL is valid"""
    pass


class URLIsReachableAction(Action):
    """Check if URL is reachable"""
    pass


class URLWithHTTPResponseStatusCodeAction(Action):
    """Check is upplied URL responds with expected HTTP response status code

    Params:
        Expected HTTP Response Status Code

    """
    pass
