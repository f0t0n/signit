import pytest
import signit


@pytest.fixture(scope='module')
def _key_settings():
    return {
        'key_length': 5,
        'key_chars': 'abc123',
    }


def test_generate_key(_key_settings):
    key = signit.key.generate(**_key_settings)
    assert (len(key) == _key_settings['key_length'],
            'Key should have defined length')
    assert (not set(key) - set(_key_settings['key_chars']),
            'Key should contain only defined chars')
