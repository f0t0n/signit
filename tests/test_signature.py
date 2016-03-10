import pytest
from signit import create_signature
from signit import parse_signature
from signit import verify_signature
from signit import generate_key


@pytest.fixture(scope='module')
def state():
    signature = (
        '0947c88ce16d078dde4a2aded1fe4627643a378757dccc3428c19569fea99542'
    )
    prefix = 'HMAC-SHA256'
    access_key = 'my access key'
    secret_key = 'my secret key'
    message = '1457369891.672671'
    full_signature = '{} {}:{}'.format(prefix, access_key, signature)
    return dict(message=message,
                access_key=access_key,
                secret_key=secret_key,
                signature=signature,
                full_signature=full_signature)


def test_generate_key():
    key_settings = {
        'key_length': 5,
        'key_chars': 'abc123',
    }
    key = generate_key(**key_settings)
    assert (len(key) == key_settings['key_length'],
            'Key should have defined length')
    assert (not set(key) - set(key_settings['key_chars']),
            'Key should contain only defined chars')


def test_create_signature(state):
    expected_result = state['full_signature']
    actual_result = create_signature(state['access_key'], state['secret_key'],
                                     state['message'])
    assert actual_result == expected_result, 'Should produce correct signature'


def test_parse_signature(state):
    access_key, signature = parse_signature(state['full_signature'])
    assert (
        (access_key, signature) == (state['access_key'], state['signature']),
        'Should parse access key and signature correctly'
    )
    with pytest.raises(ValueError) as e:
        parse_signature(state['full_signature'], auth_header_prefix='my pref')
    assert 'Invalid prefix value in `Authorization` header.' in str(e.value)


def test_verify_signature(state):
    valid = (state['access_key'], state['secret_key'], state['message'],
             state['full_signature'])
    invalid = (
        (state['access_key'], state['secret_key'], state['message'] + 'x',
         state['full_signature']),
        (state['access_key'] + 'x', state['secret_key'],
         state['message'], state['full_signature']),
        (state['access_key'], state['secret_key'] + 'x',
         state['message'], state['full_signature']),
        (state['access_key'], state['secret_key'], state['message'],
         state['full_signature'] + 'x')
    )
    assert verify_signature(*valid)
    for args in invalid:
        assert not verify_signature(*args)
