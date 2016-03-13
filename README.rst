Signit
======

|Build Status| |Coverage Status| |PyPI version|

**Signit** is a helper-library to create and verify HMAC (HMAC-SHA256 by
default) signatures that could be used to sign requests to the APIs.

`Documentation <http://f0t0n.github.io/signit>`__

On the **client** side you could

* sign your requests using ``signit.signature.create()``

On the **server** side you could

* parse a signature retrieved from request header or query string using
  ``signit.signature.parse()``
* verify retrieved signature using ``signit.signature.verify()``
* generate access and secret keys for client using ``signit.key.generate()``

--------------

Example of usage (Py3k):
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import datetime
    import requests
    import signit

    ACCESS_KEY = 'MY_ACCESS_KEY'
    SECRET_KEY = 'MY_SECRET_KEY'

    def create_user(user: dict) -> bool:
        msg = str(datetime.datetime.utcnow().timestamp())
        auth = signit.signature.create(MY_ACCESS_KEY, MY_SECRET_KEY, msg)
        headers = {
            'Unix-Timestamp': msg,
            'Authorization': auth,
        }
        r = requests.post('http://example.com/users', json=user, headers=headers)
        return r.status_code == 201

The ``Authorization`` header will look like

.. code:: http

    Authorization: HMAC-SHA256 MY_ACCESS_KEY:0947c88ce16d078dde4a2aded1fe4627643a378757dccc3428c19569fea99542

--------------

The server has issued access key and secret key for you. And only you
and the server know the secret key.

So that the server could identify you by your public access key and
ensure that you used the secret key to produce a hash of the message in
this way:

.. code:: python

    # ...somewhere in my_api/resources/user.py
    import signit
    from aiohttp import web
    from psycopg2 import IntegrityError

    async def post(request):
        message = request.headers['Unix-Timestamp']
        access_key, signature = signit.signature.parse(request.headers['Authorization'])
        secret_key = await get_secret_key_from_db(access_key)
        if not signit.signature.verify(access_key, secret_key, message, signature):
            raise web.HTTPUnauthorized('Invalid signature')
        try:
            await create_user(request)
        except IntegrityError:
            raise web.HTTPConflict()
        return web.HTTPCreated()

Additionally if you use a ``Unix-Timestamp`` for message the server
could check if the request is too old and respond with ``401`` to
protect against "replay attacks".

.. |Build Status| image:: https://travis-ci.org/f0t0n/signit.svg?branch=master
   :target: https://travis-ci.org/f0t0n/signit
.. |Coverage Status| image:: https://coveralls.io/repos/github/f0t0n/signit/badge.svg?branch=master
   :target: https://coveralls.io/github/f0t0n/signit?branch=master
.. |PyPI version| image:: https://badge.fury.io/py/signit.svg
   :target: https://badge.fury.io/py/signit
