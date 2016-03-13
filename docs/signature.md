# Signature
---

#### Module description

The module **``signit.signature``** implements a functionality that allows you to create HMAC signature, parse generated signatures and validate the signature (e.g. provided by your API client) against known message, access key and secret key.

---

#### Module interface

> **``signit.signature.create(access_key, secret_key, message, algorithm=sha256, auth_header_prefix=AUTH_PREFIX_HEADER)``**

Creates a HMAC signature to pass to `Authorization` header or query string.

**Parameters:**

- **access_key** (*str*) - A public access key that allows to identify the client
- **secret_key** (*str*) - A private secret key to hash the message with
- **message** (*str*) - A message to hash
- **algorithm** - Is the digest name, digest constructor or module for the HMAC object to use (default ``hashlib.sha256``). For more details see [*``hmac.new``*](https://docs.python.org/3.5/library/hmac.html#hmac.new)

**Returns** (*str*) - a generated signature in format of `'<prefix> <access key>:<hmac signature>'`

---

> **``signit.signature.parse(signature, auth_header_prefix=None)``**

Parses a signature created before with ``signit.signature.create``.

**Parameters:**

- **signature** (*str*) - a signature to parse
- **auth_header_prefix** (*str*) - a header prefix you expect signature to have. If set, the ``ValueError`` will be raised if the ``signature`` has different prefix.

**Returns** (*tuple*) - ``(<access_key>, <hmac_signature>)`` tuple

---

> **``signit.signature.verify(access_key, secret_key, message, signature,
           auth_header_prefix=AUTH_PREFIX_HEADER)``**

Verifies the signature (e.g. provided by API client) against known ``access_key``, ``secret_key`` and ``message``. 

In other words it allows the server side to make sure the ``message`` has been hashed with an appropriate ``secret_key`` that belongs to the client identified by its ``access_key``.

**Parameters:**

- **access_key** (*str*) - A public access key that allows to identify the client
- **secret_key** (*str*) - A private secret key to hash the message with
- **message** (*str*) - A message to hash
- **signature** (*str*) - A signature provided by client in format of ``'<prefix> <access key>:<hmac signature>'``
- **auth_header_prefix** - a header prefix you're expect to see in provided ``signature`` to reproduce its (signature's) exact copy during the verification.

**Returns** (*bool*) - is the provided `signature` valid, namely is successfully verified against known on the server side access, secret key and the message.
