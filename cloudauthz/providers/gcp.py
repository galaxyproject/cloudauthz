"""
Implements means of assuming a Google Cloud Platform (GCP)
service account to obtain temporary access token to access
GCP resources.
"""

import urllib

from ..interfaces.providers import *


class Authorize(IProvider):

    def __init__(self, config):
        self.config = None
        super(Authorize, self).__init__(config)

    def expand_config(self, config):
        self.config = {
            "type": "service_account",
            "project_id": config["project_id"],
            "private_key_id": config["private_key_id"],
            "private_key": config["private_key"],
            "client_email": config["client_email"],
            "client_id": config["client_id"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/".format(
                urllib.quote(config["client_email"]))
        }

    def get_credentials(self):
        return self.config
