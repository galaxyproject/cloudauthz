"""
Implements means of exchanging client credentials with temporary access token to access Azure.
"""

from ..interfaces.providers import *

import adal

class Authorize(IProvider):
    AUTH_ENDPOINT = "https://login.microsoftonline.com/{}"
    RESOURCE = "https://storage.azure.com/"

    def get_credentials(self, tenant_id, client_id, client_secret):
        authority_url = self.AUTH_ENDPOINT.format(tenant_id)
        context = adal.AuthenticationContext(
            authority_url,
            validate_authority=tenant_id != 'adfs',
            api_version=None,
            verify_ssl=False)

        return context.acquire_token_with_client_credentials(self.RESOURCE, client_id, client_secret)
