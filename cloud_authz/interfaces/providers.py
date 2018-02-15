"""
Implements interface(s) for authorization to cloud-based resource providers.
"""

from abc import ABCMeta, abstractmethod


class IProvider:
    """
    Interface for classes implementing means to authorize on cloud-based resource providers.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_credentials(self, **kwargs):
        """
        Implements means of obtaining credentials to access resources on the provider.

        :param kwargs: each provider could require a different set of parameters to
        authorize an access; therefore, kwargs is a dictionary of all the required
        parameters for the provider. For instance, AWS requires the following parameters:
        - identity token; OpenID Connect ID token;
        - Role ARN; amazon resource name for a role to assume.

        :rtype:  dict
        :return: credentials to access resources on the provider.
        """
        raise NotImplementedError
