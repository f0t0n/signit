import string

AUTH_PREFIX_HEADER = 'HMAC-SHA256'
KEY_CHARS = string.ascii_letters + string.digits
KEY_LENGTH = 32
SIGNATURE_FORMAT = '{auth_header_prefix} {access_key}:{hmac_hex_digest}'
UTF8 = 'utf-8'
