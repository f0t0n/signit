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
- **algorithm** - Is the digest name, digest constructor or module for the HMAC object to use (default ``hashlib.sha256``). For more details see [*``hmac.new``*](https://docs.python.org/3.5/library/hmac.html#hmac.new). Used to create a HMAC.
- **auth_header_prefix** (*str*) - A prefix for ``Authorization`` header (default ``'HMAC-SHA256'``).

**Returns** (*str*) - a generated signature in format of `'<auth_header_prefix> <access_key>:<hmac_hex_digest>'`

---

> **``signit.signature.parse(signature)``**

Parses a signature created before with ``signit.signature.create``.

**Parameters:**

- **signature** (*str*) - a signature to parse (the value from ``Authorization`` header).

**Returns** (*list*) - Signagure's parts in form of ``[<auth_header_prefix>, <access_key>, <hmac_hex_digest>]``.

---

> **``signit.signature.verify(hmac_hex_digest, secret_key, message, algorithm=sha256)``**

Verifies the signature (e.g. provided by API client) against known ``secret_key`` and ``message``. 

In other words it allows the server side to make sure the ``message`` has been hashed with an appropriate ``secret_key``.

**Parameters:**

- **hmac_hex_digest** (*str*) - A message's hash to check.
Namely it's ``<hmac_hex_digest>`` part from the ``Authorization`` header's value (``'<auth_header_prefix> <access_key>:<hmac_hex_digest>'``).
- **secret_key** (*str*) - A private secret key to hash the message with.
- **message** (*str*) - A message to hash.
- **algorithm** - Is the digest name, digest constructor or module for the HMAC object to use (default ``hashlib.sha256``). For more details see [*``hmac.new``*](https://docs.python.org/3.5/library/hmac.html#hmac.new). Used to create a HMAC.

**Returns** (*bool*) - is the provided `hmac_hex_digest` valid, namely is successfully verified against known on the server side secret key and the message.
