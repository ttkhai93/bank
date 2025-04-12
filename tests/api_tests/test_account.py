import pytest

from tests.utils import parse_response_body

from core.repositories import UserRepository, AssetRepository


@pytest.fixture
async def user():
    json = {"email": "user@example.com", "password": "123456"}
    return await UserRepository.create(json)


@pytest.fixture
async def asset():
    json = {"code": "example", "name": "example"}
    return await AssetRepository.create(json)


async def test_get_account(new_client):
    res = await new_client.get("/accounts")
    data, _ = parse_response_body(res)
    accounts = data.get("accounts")

    assert len(accounts) == 0


async def test_create_account(new_client, asset, user):
    json = {"user_id": str(user["id"]), "asset_id": str(asset["id"])}
    res = await new_client.post("/accounts", json=json)
    data, message = parse_response_body(res)
    account = data.get("account")

    assert json["user_id"] == account["user_id"]
    assert json["asset_id"] == account["asset_id"]
