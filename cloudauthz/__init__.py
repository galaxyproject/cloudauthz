"""
Implements means of delegating access to cloud-based resources.
"""

__version__ = "0.3.0"

from .providers import aws
from .providers import azure
from .providers import gcp


class CloudAuthz:

    def __init__(self):
        pass

    def authorize(self, provider, config):
        if provider.lower() == "aws":
            authz = aws.Authorize()
            authz.assert_config(config)
            return authz.get_credentials(
                config['id_token'],
                config['role_arn'],
                config.get('role_session_duration', 900),
                config.get('role_session_name', 'cloudauthz'))
        elif provider.lower() == "azure":
            authz = azure.Authorize()
            authz.assert_config(config)
            return authz.get_credentials(config["tenant_id"], config["client_id"], config["client_secret"])
        elif provider.lower() == "gcp":
            authz = gcp.Authorize()
            authz.assert_config(config)
            return authz.get_credentials(
                config["client_service_account"],
                config["server_service_account_credentials_filename"])
        else:
            raise NotImplementedError("Authorization flow for the provider `{}` is not implemented.".format(provider))
