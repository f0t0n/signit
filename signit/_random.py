from time import time
from random import SystemRandom


def get_random_sequence(length, source_sequence):
    return (SystemRandom(time()).choice(source_sequence)
            for x in range(length))


def get_random_string(length, source_sequence):
    return ''.join(get_random_sequence(length, source_sequence))
