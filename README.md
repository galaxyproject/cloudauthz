# CloudAuthz

## Installation
Install the latest release from PyPi:

    pip install cloudauthz


## Example

CloudAuthz can authorize access to [Amazon Web Services (AWS)](#amazon-web-services), [Microsoft Azure](#microsoft-azure), and [Google Cloud Platform (GCP)](#google-cloud-platform). An example for each provider is given in the following.

- ### Amazon Web Services

    ```python
    from cloudauthz import *
    
    cloudauthz = CloudAuthz()
    config = {
        "id_token": " ... ",
        "role_arn": " ... "
    }
    credentials = cloudauthz.authorize("aws", config)
    ```
    
    The `credentials` object is a dictionary as the following:
    
    ```json
    {
      "SecretAccessKey": " ... ", 
      "SessionToken": " ... ", 
      "Expiration": "2019-05-28T02:12:45Z", 
      "AccessKeyId": " ... "
    }
    ```

- ### Microsoft Azure

    ```python
    from cloudauthz import *
    
    cloudauthz = CloudAuthz()
    config = {
        "tenant_id": " ... ",
        "client_id": " ... ",
        "client_secret": " ... "
    }
    credentials = cloudauthz.authorize("azure", config)
    ```
    
    The `credentials` object is a dictionary as the following:
    
    ```json
    {
        "expiresIn": 3599,
        "_authority": "https://login.microsoftonline.com/TENANT_ID",
        "resource": "https://storage.azure.com/",
        "tokenType": "Bearer",
        "expiresOn": "2018-06-28 12:30:24.895661",
        "isMRRT": true,
        "_clientId": " ... ",
        "accessToken": " ... ",
    }
    ```

- ### Google Cloud Platform

    ```python
    from cloudauthz import *
    
    cloudauthz = CloudAuthz()
    config = {
        "project_id": "...",
        "private_key_id": "...",
        "private_key": "...",
        "client_email": "...",
        "client_id": "..."
    }
    credentials = cloudauthz.authorize("gcp", config)
    ```
    
    The `credentials` object is a dictionary containing the following keys:
    
    ```json
    {
      "type": "service_account",
      "project_id": "...",
      "private_key_id": "...",
      "private_key": "...",
      "client_email": "...",
      "client_id": "...",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "..."
    }
    ```
