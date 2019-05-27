"""
Wraps exceptions for authorizing and/or exchanging tokens.
"""


class CloudAuthzBaseException(ValueError):
    """
    Base class for all the exceptions thrown (or relayed) in CloudAuthnz.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class InvalidTokenException(CloudAuthzBaseException):
    """
    Represents errors that occur during ID token utilization.
    """
    def __init__(self, message):
        CloudAuthzBaseException.__init__(self, message)


class ExpiredTokenException(CloudAuthzBaseException):
    """
    Represents errors that occur when utilizing expired tokens.
    """
    def __init__(self, message):
        CloudAuthzBaseException.__init__(self, message)


class AccessDeniedException(CloudAuthzBaseException):
    """
    Represents errors that occur when accessing resources that
    the either the user is not allowed to, or if any of the
    resources is miss-spelled.
    """
    def __init__(self, message):
        CloudAuthzBaseException.__init__(self, message)

    def __str__(self):
        return self.message + ". You may not have access to the resource, or miss-spelled a configuration " \
                              "(e.g., incorrect amazon resource name, or an incorrect `aud` (Audience) is " \
                              "set on the resource provider)."


class InvalidRequestException(CloudAuthzBaseException):
    """
    Represents errors that occur when an invalid request is made
    to the resource provider. For instance, an invalid `Tenant name`
    on Microsoft Azure.
    """
    def __init__(self, message):
        CloudAuthzBaseException.__init__(self, message)