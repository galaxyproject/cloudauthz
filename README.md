# CloudAuthz

## Installation
Install the latest release from PyPi:

    pip install cloudauthz


## Example

An example on using Microsoft Azure backend: 

```python
from cloudauthz import *

ca = CloudAuthz()
res = ca.authorize('azure', {'tenant_id': TENANT_ID,
                             'client_id': CLIENT_ID,
                             'client_secret': CLIENT_SECRET})
```

An example of `res` is as the following: 

```python
{
    'expiresIn': 3599,
    '_authority': 'https://login.microsoftonline.com/TENANT_ID',
    'resource': u'https://storage.azure.com/',
    'tokenType': u'Bearer',
    'expiresOn': '2018-06-28 12:30:24.895661',
    'isMRRT': True,
    '_clientId': CLIENT_ID,
    'accessToken': AN_ACCESS_TOKEN,
}
```
