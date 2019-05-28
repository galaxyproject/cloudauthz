"""
Implements means of exchanging user ID token with temporary access and secret key.
"""

import xml.etree.ElementTree as ET
import requests

from ..exceptions import *
from ..interfaces.providers import *


class Authorize(IProvider):

    action = "AssumeRoleWithWebIdentity"
    version = "2011-06-15"
    namespace = '{https://sts.amazonaws.com/doc/2011-06-15/}'

    def __init__(self, config):
        self.identity_token = None
        self.role_arn = None
        self.token_ttl = None
        self.role_session_name = None
        super(Authorize, self).__init__(config)

    def __parse_error(self, response):
        """
        Parses the AWS STS xml-based error response, and throws appropriate exception.

        :type  response: string
        :param response: error xml

        :rtype : CloudAuthzBaseException (or any of its derived classes)
        :return: a CloudAuthz exception w.r.t. AWS STS error code.
        """
        root = ET.fromstring(response)
        error = root.find('{}Error'.format(self.namespace))
        code = error.find('{}Code'.format(self.namespace)).text
        message = error.find('{}Message'.format(self.namespace)).text
        if code == 'ExpiredTokenException':
            return ExpiredTokenException(message)
        elif code == 'AccessDenied':
            return AccessDeniedException(message)
        elif code == 'InvalidIdentityToken':
            return InvalidTokenException(message)
        else:
            return CloudAuthzBaseException(message)

    def expand_config(self, config):
        """
        Asserts if the config dictionary contains all the
        keys necessary for the AWS authorization flow; and
        sets all the necessary and optional parameters.

        :type   config: dict
        :param  config: a dictionary containing all the
        necessary and optional parameters for AWS authorization
        flow. The expected keys are as the following:

            -   identity_token: an OpenID Connect identity
            token represented in JSON Web Token (JWT) format.

            -   role_arn:  an Amazon Resource Name (ARN)
            of a role to be assumed.

            -   duration:   an integer specifying the
            session duration in seconds; ; credentials will
            expire after this period. Valid values range
            from 900 seconds to 3600 seconds.

            -   role_session_name:  a name assigned to the
            session, consisting of lower and upper-case
            letters with no space.

        :return: all the optional and required parameters.
        """
        if 'id_token' not in config:
            raise KeyError("`id_token` is not provided.")
        self.identity_token = config['id_token']

        if 'role_arn' not in config:
            raise KeyError("`role_arn` is not provided.")
        self.role_arn = config['role_arn']

        self.token_ttl = config.get('token_ttl', 900)
        self.role_session_name = config.get('role_session_name', 'cloudauthz')

    def get_credentials(self):
        """
        Assumes an AWS Role and returns credentials accordingly.

        :rtype : dict
        :return: a dictionary containing credentials to access the resources
        available to the assumed role. Credentials are:
        - Access Key ID
        - Secret Access Key
        - Session Token
        """
        url = "https://sts.amazonaws.com/?" \
              "DurationSeconds={}&" \
              "Action={}&Version={}&" \
              "RoleSessionName={}&" \
              "RoleArn={}&" \
              "WebIdentityToken={}"\
            .format(self.token_ttl,
                    self.action,
                    self.version,
                    self.role_session_name,
                    self.role_arn,
                    self.identity_token)
        response = requests.get(url)

        if response.ok:
            root = ET.fromstring(response.content)
            rtv = {}
            role_assume_result = root.find('{}AssumeRoleWithWebIdentityResult'.format(self.namespace))
            credentials = role_assume_result.find('{}Credentials'.format(self.namespace))
            for attribute in credentials:
                rtv[attribute.tag.replace(self.namespace, '')] = attribute.text
            return rtv
        else:
            raise self.__parse_error(response.content)
