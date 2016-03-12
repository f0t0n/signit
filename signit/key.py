from random import SystemRandom
from ._constants import KEY_CHARS
from ._constants import KEY_LENGTH


def generate(key_length=KEY_LENGTH, key_chars=KEY_CHARS):
    rand = SystemRandom()
    return ''.join((rand.choice(key_chars) for x in range(key_length)))
