"""
Wraps exceptions for authorizing and/or exchanging tokens.
"""


class CloudAuthzBaseException(ValueError):
    """
    Base class for all the exceptions thrown (or relayed) in CloudAuthnz.
    """

    pass


class InvalidTokenException(CloudAuthzBaseException):
    """
    Represents errors that occur during ID token utilization.
    """

    def __str__(self):
        return "The ID token is invalid."


class ExpiredTokenException(CloudAuthzBaseException):
    """
    Represents errors that occur when utilizing expired tokens.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
