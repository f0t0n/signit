import pytest
import signit


@pytest.fixture(scope='module')
def _prefix():
    return 'HMAC-SHA256'


@pytest.fixture(scope='module')
def _access_key():
    return 'my access key'


@pytest.fixture(scope='module')
def _secret_key():
    return 'my secret key'


@pytest.fixture(scope='module')
def _message():
    return '1457369891.672671'


@pytest.fixture(scope='module')
def _hmac_digest():
    return '0947c88ce16d078dde4a2aded1fe4627643a378757dccc3428c19569fea99542'


@pytest.fixture(scope='module')
def _full_signature(_prefix, _access_key, _hmac_digest):
    return '{} {}:{}'.format(_prefix, _access_key, _hmac_digest)


def test_create(_access_key, _secret_key, _message, _full_signature):
    expected_result = _full_signature
    actual_result = signit.signature.create(_access_key, _secret_key, _message)
    assert actual_result == expected_result, 'Should produce correct signature'


def test_parse(_prefix, _access_key, _hmac_digest, _full_signature):
    prefix, access_key, hmac_digest = signit.signature.parse(_full_signature)
    assert (
        (prefix, access_key, hmac_digest) == (_prefix, _access_key,
                                              _hmac_digest),
        'Should parse prefix, access key and hmac digest correctly'
    )


def test_verify(_hmac_digest, _secret_key, _message):
    valid = (_hmac_digest, _secret_key, _message)

    def _invalid(wrong_index):
        args = list(valid)
        arg = args.pop(wrong_index)
        args.insert(wrong_index, arg + 'x')
        return args

    invalid = (_invalid(i) for i, val in enumerate(valid))

    assert signit.signature.verify(*valid)

    for args in invalid:
        assert not signit.signature.verify(*args)
