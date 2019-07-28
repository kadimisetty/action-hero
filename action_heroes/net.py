from argparse import Action


class IPIsValidIPv4AddressAction(Action):
    """Check if IP is valid ipv4 address"""

    def __call__(self):
        raise NotImplementedError


class IPIsValidIPV6Action(Action):
    """Check if IP is valid ipv6 address"""

    def __call__(self):
        raise NotImplementedError


class IPIsValidIPAction(Action):
    """Check if URL is valid"""

    def __call__(self):
        raise NotImplementedError


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
