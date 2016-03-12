import string

AUTH_PREFIX_HEADER = 'HMAC-SHA256'
KEY_CHARS = string.ascii_letters + string.digits
KEY_LENGTH = 32
SIGNATURE_FORMAT = '{prefix} {access_key}:{signature}'
UTF8 = 'utf-8'
