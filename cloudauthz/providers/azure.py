"""
Implements means of exchanging client credentials with temporary access token to access Azure.
"""

import adal

from ..exceptions import *
from ..interfaces.providers import *


class Authorize(IProvider):
    AUTH_ENDPOINT = "https://login.microsoftonline.com/{}"
    RESOURCE = "https://storage.azure.com/"

    def __init__(self, config):
        self.tenant_id = None
        self.client_id = None
        self.client_secret = None
        super(Authorize, self).__init__(config)

    def __parse_error(self, exception):
        if isinstance(exception, adal.adal_error.AdalError):
            return InvalidRequestException(str(exception.error_response))

    def expand_config(self, config):
        if "tenant_id" not in config:
            raise KeyError("`tenant_id` is not provided.")
        self.tenant_id = config["tenant_id"]

        if "client_id" not in config:
            raise KeyError("`client_id` is not provided.")
        self.client_id = config["client_id"]

        if "client_secret" not in config:
            raise KeyError("`client_secret` is not provided.")
        self.client_secret = config["client_secret"]

    def get_credentials(self):
        authority_url = self.AUTH_ENDPOINT.format(self.tenant_id)
        context = adal.AuthenticationContext(
            authority_url,
            validate_authority=self.tenant_id != 'adfs',
            api_version=None,
            verify_ssl=False)
        try:
            return context.acquire_token_with_client_credentials(
                self.RESOURCE,
                self.client_id,
                self.client_secret)
        except Exception as e:
            raise self.__parse_error(e)
