"""
Implements interface(s) for authorization to cloud-based resource providers.
"""

from abc import ABCMeta, abstractmethod


class IProvider:
    """
    Interface for classes implementing means to authorize on cloud-based resource providers.
    """

    __metaclass__ = ABCMeta

    def __init__(self, config):
        self.expand_config(config)

    @abstractmethod
    def expand_config(self, config):
        """
        Asserts if the config dictionary contains all the keys
        necessary for obtaining credentials from the provider,
        and raises an exception if a required key is missing,
        or if the value of a key does not adhere to expected
        format.

        Upon a successful assertion, it sets all the required and
        optional keys for the provider's authorization flow.

        :type  config:  dict
        :param config:  contains all the information necessary
        for obtaining temporary credentials from the provider.

        :return: void
        """
        raise NotImplementedError

    @abstractmethod
    def get_credentials(self, config):
        """
        Implements means of obtaining credentials to access resources on the provider.

        :type   config: dict
        :param  config: contains provider-specific parameters
        required to authorize client access. The `expand_config`
        method should be used to assert if the `config` dictionary
        contains all the keys required for the provider's
        authorization flow.

        :rtype:  dict
        :return: credentials to access resources on the provider.
        """
        raise NotImplementedError
