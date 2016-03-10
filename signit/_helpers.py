from ._constants import UTF8


def _bytes(_str, encoding=UTF8):
    return _str.encode(encoding)
