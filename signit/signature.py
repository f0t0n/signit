import hmac
from hashlib import sha256
from ._constants import AUTH_PREFIX_HEADER
from ._constants import SIGNATURE_FORMAT
from ._helpers import _bytes


def _create_digest(secret_key, message, algorithm=sha256):
    new_hmac = hmac.new(_bytes(secret_key), msg=_bytes(message),
                        digestmod=algorithm)
    return new_hmac.hexdigest()


def create(access_key, secret_key, message, algorithm=sha256,
           auth_header_prefix=AUTH_PREFIX_HEADER):
    hmac_hex_digest = _create_digest(secret_key, message, algorithm=algorithm)
    return SIGNATURE_FORMAT.format(auth_header_prefix=auth_header_prefix,
                                   access_key=access_key,
                                   hmac_hex_digest=hmac_hex_digest)


def parse(signature):
    """ Parses the header value
    and returns a list (<auth_header_prefix>, <access_key>, <hmac_hex_digest>).
    """
    prefix, access_key_hmac_digest = signature.split(' ', 1)
    return [prefix] + access_key_hmac_digest.split(':')


def verify(hmac_hex_digest, secret_key, message, algorithm=sha256):
    valid_hmac_hex_digest = _create_digest(secret_key, message,
                                           algorithm=algorithm)
    return hmac.compare_digest(hmac_hex_digest, valid_hmac_hex_digest)
