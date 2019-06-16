"""
Implements means of assuming a Google Cloud Platform (GCP)
service account to obtain temporary access token to access
GCP resources.
"""

import httplib2
import json
import os

from apiclient.discovery import build
from googleapiclient import errors
from oauth2client.client import AccessTokenCredentials
from oauth2client.client import GoogleCredentials

from ..exceptions import *
from ..interfaces.providers import *


class Authorize(IProvider):
    PRJ_ID_WILDCARD_CHAR = '-'
    SCOPES = ["https://www.googleapis.com/auth/iam",
              "https://www.googleapis.com/auth/cloud-platform"]
    CREDS_ENV_VAR = "GOOGLE_APPLICATION_CREDENTIALS"

    def __init__(self, config):
        self.token_ttl = None
        self.client_service_account = None
        self.creds_filename = None
        super(Authorize, self).__init__(config)

    def __parse_error(self, response):
        try:
            response = json.loads(response.content)
            details = response
            error_code = response["error"]["code"]
            messages = []
            for m in response["error"]["errors"]:
                hint = ""
                if "Requested entity was not found" in m["message"]:
                    hint = " (hint: you may have misspelled the client service account name.)"
                messages.append(m["message"] + hint)
            messages = ', '.join(messages)
            if error_code == 404:
                return InvalidRequestException(messages, error_code, details)
            else:
                return CloudAuthzBaseException(messages, error_code, details)
        except:
            return CloudAuthzBaseException(response)

    def expand_config(self, config):
        if "client_service_account" not in config:
            raise KeyError("`client_service_account` is not provided.")
        self.client_service_account = config["client_service_account"]

        if "server_credentials" not in config:
            raise KeyError("`server_credentials` is not provided.")
        self.creds_filename = config["server_credentials"]

        self.token_ttl = config.get('token_ttl', 3600)

    def get_credentials(self):
        os.environ[self.CREDS_ENV_VAR] = self.creds_filename
        jw_access_credentials = GoogleCredentials.get_application_default()
        if jw_access_credentials.create_scoped_required():
            jw_access_credentials = jw_access_credentials.create_scoped(" ".join(self.SCOPES))
        http = jw_access_credentials.authorize(httplib2.Http())

        body = {
            "delegates": [],
            "scope": self.SCOPES[1],
            "lifetime": "{}s".format(self.token_ttl)
        }

        try:
            access_token = build(
                serviceName='iamcredentials',
                version='v1',
                http=http
            ).projects().serviceAccounts().generateAccessToken(
                name="projects/{}/serviceAccounts/{}".format(
                    self.PRJ_ID_WILDCARD_CHAR,
                    self.client_service_account),
                body=body
            ).execute()["accessToken"]

            credentials = AccessTokenCredentials(access_token, "MyAgent/1.0", None)
            return credentials
        except errors.HttpError as e:
            raise self.__parse_error(e)
