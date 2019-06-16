"""
Implements means of delegating access to cloud-based resources.
"""

__version__ = "0.4.0"

from .providers import aws
from .providers import azure
from .providers import gcp


class CloudAuthz:

    def __init__(self):
        pass

    def authorize(self, provider, config):
        if provider.lower() == "aws":
            authz = aws.Authorize(config)
        elif provider.lower() == "azure":
            authz = azure.Authorize(config)
        elif provider.lower() == "gcp":
            authz = gcp.Authorize(config)
        else:
            raise NotImplementedError("Authorization flow for the provider `{}` is not implemented.".format(provider))
        return authz.get_credentials()
