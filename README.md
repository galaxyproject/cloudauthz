# CloudAuthz

## Installation
Install the latest release from PyPi:

    pip install cloudauthz


## Example

Using AWS backend: 

```python
from cloudauthz import *

cloudauthz = CloudAuthz()
config = {
    "id_token": " ... ",
    "role_arn": " ... "
}
credentials = cloudauthz.authorize("aws", config)
```

an example of the `credentials` is as following:

```json
{
  "SecretAccessKey": " ... ", 
  "SessionToken": " ... ", 
  "Expiration": "2019-05-28T02:12:45Z", 
  "AccessKeyId": " ... "
}
```

An example on using Microsoft Azure backend: 

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

An example of `res` is as the following: 

```json
{
    "expiresIn": 3599,
    "_authority": "https://login.microsoftonline.com/TENANT_ID",
    "resource": "https://storage.azure.com/",
    "tokenType": "Bearer",
    "expiresOn": "2018-06-28 12:30:24.895661",
    "isMRRT": True,
    "_clientId": " ... ",
    "accessToken": " ... ",
}
```


An example of using Google Cloud Platform (GCP) backend:

```python
from cloudauthz import *

cloudauthz = CloudAuthz()
config = {
    "client_service_account": " ... ", 
    "server_service_account_credentials_filename": " ... "}
credentials = cloudauthz.authorize("gcp", config)
```

The `credentials` object is an instance of `oauth2client.client.AccessTokenCredentials`.
GCP clients can be constructed using this object; however, if an access token is required, 
you may obtain one using the `access_token` property of this instance:

```python
credentials.access_token
```
