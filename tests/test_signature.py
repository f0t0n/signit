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
def _signature():
    return '0947c88ce16d078dde4a2aded1fe4627643a378757dccc3428c19569fea99542'


@pytest.fixture(scope='module')
def _full_signature(_prefix, _access_key, _signature):
    return '{} {}:{}'.format(_prefix, _access_key, _signature)


def test_create(_access_key, _secret_key, _message, _full_signature):
    expected_result = _full_signature
    actual_result = signit.signature.create(_access_key, _secret_key, _message)
    assert actual_result == expected_result, 'Should produce correct signature'


def test_parse(_access_key, _signature, _full_signature):
    access_key, signature = signit.signature.parse(_full_signature)
    assert (
        (access_key, signature) == (_access_key, _signature),
        'Should parse access key and signature correctly'
    )
    with pytest.raises(ValueError) as e:
        signit.signature.parse(_full_signature,
                               auth_header_prefix='WRONG_PREFIX')
    assert 'Invalid prefix value in `Authorization` header.' in str(e.value)


def test_verify(_access_key, _secret_key, _message, _full_signature):
    valid = (_access_key, _secret_key, _message, _full_signature)
    len_valid = len(valid)

    def _invalid(wrong_index):
        args = list(valid)
        arg = args.pop(wrong_index)
        args.insert(wrong_index, arg + 'x')
        return args

    invalid = (_invalid(i) for i in range(len_valid - 1))

    assert signit.signature.verify(*valid)

    for args in invalid:
        assert not signit.signature.verify(*args)
