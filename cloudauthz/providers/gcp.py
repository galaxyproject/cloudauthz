"""
Implements means of assuming a Google Cloud Platform (GCP)
service account to obtain temporary access token to access
GCP resources.
"""

import os
import httplib2

from apiclient.discovery import build
from oauth2client.client import AccessTokenCredentials
from oauth2client.client import GoogleCredentials

from ..interfaces.providers import *


class Authorize(IProvider):
    PRJ_ID_WILDCARD_CHAR = '-'
    SCOPES = ["https://www.googleapis.com/auth/iam",
              "https://www.googleapis.com/auth/cloud-platform"]
    CREDS_ENV_VAR = "GOOGLE_APPLICATION_CREDENTIALS"

    def assert_config(self, config):
        if "client_service_account" not in config:
            raise KeyError("`client_service_account` is not provided.")
        if "server_service_account_credentials_filename" not in config:
            raise KeyError("`server_service_account_credentials_filename` is not provided.")

    def get_credentials(self, client_service_account,
                        server_service_account_credentials_filename,
                        token_ttl=3600):

        os.environ[self.CREDS_ENV_VAR] = server_service_account_credentials_filename
        jw_access_credentials = GoogleCredentials.get_application_default()
        if jw_access_credentials.create_scoped_required():
            jw_access_credentials = jw_access_credentials.create_scoped(" ".join(self.SCOPES))
        http = jw_access_credentials.authorize(httplib2.Http())

        body = {
            "delegates": [],
            "scope": self.SCOPES[1],
            "lifetime": "{}s".format(token_ttl)
        }

        access_token = build(
            serviceName='iamcredentials',
            version='v1',
            http=http
        ).projects().serviceAccounts().generateAccessToken(
            name="projects/{}/serviceAccounts/{}".format(
                self.PRJ_ID_WILDCARD_CHAR,
                client_service_account),
            body=body
        ).execute()["accessToken"]

        credentials = AccessTokenCredentials(access_token, "MyAgent/1.0", None)
        return credentials
