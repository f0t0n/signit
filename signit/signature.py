import hmac
from hashlib import sha256
from ._constants import AUTH_PREFIX_HEADER
from ._constants import SIGNATURE_FORMAT
from ._helpers import _bytes


def create(access_key, secret_key, message, algorithm=sha256,
           auth_header_prefix=AUTH_PREFIX_HEADER):
    new_hmac = hmac.new(_bytes(secret_key), msg=_bytes(message),
                        digestmod=algorithm)
    signature = SIGNATURE_FORMAT.format(prefix=auth_header_prefix,
                                        access_key=access_key,
                                        signature=new_hmac.hexdigest())
    return signature.strip()  # in case if `auth_header_prefix` is empty string


def parse(signature, auth_header_prefix=None):
    prefix, _signature = signature.split(' ', 1)
    if auth_header_prefix and prefix != auth_header_prefix:
        raise ValueError('Invalid prefix value in `Authorization` header.')
    return _signature.split(':')  # access_key, signature


def verify(access_key, secret_key, message, signature,
           auth_header_prefix=AUTH_PREFIX_HEADER):
    return hmac.compare_digest(
        signature,
        create(access_key, secret_key, message,
               auth_header_prefix=auth_header_prefix)
    )
