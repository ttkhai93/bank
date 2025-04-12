import pytest

from tests.utils import parse_response_body


@pytest.fixture
def user(test_client):
    json = {"email": "user@example.com", "password": "123456"}
    res = test_client.post("/users", json=json)
    data, _ = parse_response_body(res)
    user = data.get("user")
    return user


@pytest.fixture
def asset(test_client):
    json = {"code": "example", "name": "example"}
    res = test_client.post("/assets", json=json)
    data, _ = parse_response_body(res)
    asset = data.get("asset")
    return asset


def test_get_account(test_client):
    res = test_client.get("/accounts")
    data, _ = parse_response_body(res)
    accounts = data.get("accounts")

    assert len(accounts) == 0


def test_create_account(test_client, user, asset):
    json = {"user_id": str(user["id"]), "asset_id": str(asset["id"])}
    res = test_client.post("/accounts", json=json)
    data, message = parse_response_body(res)
    account = data.get("account")

    assert json["user_id"] == account["user_id"]
    assert json["asset_id"] == account["asset_id"]
