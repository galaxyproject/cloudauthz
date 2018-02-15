"""
Implements means of delegating access to cloud-based resources.
"""

__version__ = "0.0.1"

from providers import aws


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
                config.get('role_session_name', 'cloud-authz'))
        raise NotImplementedError("Authorization flow for the provider `{}` is not implemented.".format(provider))
