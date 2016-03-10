# Signit

[![Build Status](https://travis-ci.org/f0t0n/signit.svg?branch=master)](https://travis-ci.org/f0t0n/signit)
[![Coverage Status](https://coveralls.io/repos/github/f0t0n/signit/badge.svg?branch=master)](https://coveralls.io/github/f0t0n/signit?branch=master)
[![PyPI version](https://badge.fury.io/py/signit.svg)](https://badge.fury.io/py/signit)

**Signit** is a helper-library to create and verify HMAC (HMAC-SHA256 by default) signatures that could be used to sign requests to the APIs.

- As a client you could sign your requests using `signit.create_signature()`
- As a server you could verify a signature from request using `signit.verify_signature()`
- As a server you could also generate access and secret keys for your client using `signit.generate_key()`

---

### Example of usage (Py3k):

```python
import datetime
import requests
import signit

ACCESS_KEY = 'MY_ACCESS_KEY'
SECRET_KEY = 'MY_SECRET_KEY'

def create_user(user: dict) -> bool:
    msg = str(datetime.datetime.utcnow().timestamp())
    auth = signit.create_signature(MY_ACCESS_KEY, MY_SECRET_KEY, msg)
    headers = {
        'Unix-Timestamp': msg,
        'Authorization': auth,
    }
    r = requests.post('http://example.com/users', json=user, headers=headers)
    return r.status_code == 201
```

The `Authorization` header will look like
```http
Authorization: HMAC-SHA256 MY_ACCESS_KEY:0947c88ce16d078dde4a2aded1fe4627643a378757dccc3428c19569fea99542
```
---

The server has issued access key and secret key for you. And only you and the server know the secret key.

So that the server could identify you by your public access key and ensure 
that you used the secret key to produce a hash of the message in this way:

```python
# ...somewhere in my_api/resources/user.py
import signit
from aiohttp import web
from psycopg2 import IntegrityError

async def post(request):
    message = request.headers['Unix-Timestamp']
    access_key, signature = signit.parse_signature(request.headers['Authorization'])
    secret_key = await get_secret_key_from_db(access_key)
    if not signit.verify_signature(access_key, secret_key, message, signature):
        raise web.HTTPUnauthorized('Invalid signature')
    try:
        await create_user(request)
    except IntegrityError:
        raise web.HTTPConflict()
    return web.HTTPCreated()
```

Additionally if you use a `Unix-Timestamp` for message the server could 
check if the request is too old and respond with `401` to protect against "replay attacks".
