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
            if 'id_token' not in config:
                raise KeyError("`id_token` is not provided.")
            if 'role_arn' not in config:
                raise KeyError("`role_arn` is not provided.")
            return authz.get_credentials(
                config['id_token'],
                config['role_arn'],
                config.get('role_session_name', 900),
                config.get('role_session_name', 'cloudauthz'))
        elif provider.lower() == "azure":
            authz = azure.Authorize()
            if "tenant_id" not in config:
                raise KeyError("`tenant_id` is not provided.")
            if "client_id" not in config:
                raise KeyError("`client_id` is not provided.")
            if "client_secret" not in config:
                raise KeyError("`client_secret` is not provided.")
            return authz.get_credentials(config["tenant_id"], config["client_id"], config["client_secret"])
        elif provider.lower() == "gcp":
            if "client_service_account" not in config:
                raise KeyError("`client_service_account` is not provided.")
            if "server_service_account_credentials_filename" not in config:
                raise KeyError("`server_service_account_credentials_filename` is not provided.")
            authz = gcp.Authorize()
            return authz.get_credentials(
                config["client_service_account"],
                config["server_service_account_credentials_filename"])
        else:
            raise NotImplementedError("Authorization flow for the provider `{}` is not implemented.".format(provider))
