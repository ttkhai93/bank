from pytest import raises

from src.api.security.password import hash_password, check_password
from src.api.security.jwt import create_access_token, verify_access_token
from src.exceptions import UnauthorizedError


def test_hash_and_check_password_success():
    password = "<PASSWORD>"
    assert check_password(password, hash_password(password))


def test_check_password_fail():
    assert not check_password("<PASSWORD>", "123456")


def test_create_and_verify_access_token():
    user_id = "mock"
    access_token = create_access_token(user_id)
    payload = verify_access_token(access_token)
    assert user_id == payload["sub"]


def test_verify_access_token_fail():
    with raises(UnauthorizedError):
        verify_access_token("mock")
