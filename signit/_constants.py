import string

UTF8 = 'utf-8'
KEY_CHARS = string.ascii_letters + string.digits
AUTH_PREFIX_HEADER = 'HMAC-SHA256'
SIGNATURE_FORMAT = '{prefix} {access_key}:{signature}'
