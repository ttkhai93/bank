import asyncio

from pytest import mark
from fastapi import status

from core.repositories import UserRepository, AssetRepository, AccountRepository
from tests.utils import parse_response_body


async def test_get_account(new_client):
    res = await new_client.get("/v1/accounts")
    assert res.status_code == status.HTTP_200_OK

    data, _ = parse_response_body(res)
    accounts = data.get("accounts")
    assert len(accounts) == 0


async def test_get_account_by_id(new_client):
    user = await UserRepository.create({"email": "user@example.com", "password": "123456"})
    asset = await AssetRepository.create({"code": "example", "name": "example"})
    json = {"user_id": str(user["id"]), "asset_id": str(asset["id"]), "amount": 1000}
    res = await new_client.post("/v1/accounts", json=json)
    data, _ = parse_response_body(res)
    account = data.get("account")

    res = await new_client.get(f"/v1/accounts/{account['id']}")
    assert res.status_code == status.HTTP_200_OK

    data, _ = parse_response_body(res)
    assert account == data.get("account")


async def test_get_account_transactions(new_client):
    user = await UserRepository.create({"email": "user@example.com", "password": "123456"})
    asset = await AssetRepository.create({"code": "example", "name": "example"})
    json = {"user_id": str(user["id"]), "asset_id": str(asset["id"]), "amount": 1000}
    res = await new_client.post("/v1/accounts", json=json)
    data, _ = parse_response_body(res)
    account = data.get("account")

    res = await new_client.get(f"/v1/accounts/{account['id']}/transactions")
    assert res.status_code == status.HTTP_200_OK

    data, _ = parse_response_body(res)
    transactions = data.get("transactions")
    assert len(transactions) == 0


async def test_create_account(new_client):
    user = await UserRepository.create({"email": "user@example.com", "password": "123456"})
    asset = await AssetRepository.create({"code": "example", "name": "example"})

    json = {"user_id": str(user["id"]), "asset_id": str(asset["id"]), "amount": 1000}
    res = await new_client.post("/v1/accounts", json=json)
    assert res.status_code == status.HTTP_200_OK

    data, _ = parse_response_body(res)
    account = data.get("account")
    assert json["user_id"] == account["user_id"]
    assert json["asset_id"] == account["asset_id"]
    assert json["amount"] == account["amount"]
    assert 0 == account["version"]


async def test_transfer_success(new_client):
    user = await UserRepository.create({"email": "user@example.com", "password": "123456"})
    asset = await AssetRepository.create({"code": "example", "name": "example"})

    json = {"user_id": str(user["id"]), "asset_id": str(asset["id"]), "amount": 1000}
    from_account = await AccountRepository.create(json)
    to_account = await AccountRepository.create(json)

    tx_info = {"from_account_id": str(from_account["id"]), "to_account_id": str(to_account["id"]), "amount": 1000}
    res = await new_client.post("/v1/accounts/transfer", json=tx_info)
    assert res.status_code == status.HTTP_200_OK

    data, _ = parse_response_body(res)
    transaction = data.get("transaction")
    assert transaction["from_account_id"] == tx_info["from_account_id"]
    assert transaction["to_account_id"] == tx_info["to_account_id"]
    assert transaction["amount"] == tx_info["amount"]
    assert transaction["status"] == "pending"

    from_account = await AccountRepository.get_by_id(from_account["id"])
    to_account = await AccountRepository.get_by_id(to_account["id"])
    assert from_account["amount"] == json["amount"] - tx_info["amount"]
    assert to_account["amount"] == json["amount"] + tx_info["amount"]


@mark.parametrize(
    "url, concurrent_requests, expected_version",
    [
        ("/v1/accounts/transfer", 10, 0),
        ("/v2/accounts/transfer_isolation_level", 4, 0),
        ("/v2/accounts/transfer_optimistic_locking", 4, 4),
    ],
)
async def test_transfer_success_in_lost_update_scenario(new_client, url, concurrent_requests, expected_version):
    user = await UserRepository.create({"email": "user@example.com", "password": "123456"})
    asset = await AssetRepository.create({"code": "example", "name": "example"})

    json = {"user_id": str(user["id"]), "asset_id": str(asset["id"]), "amount": 1000 * concurrent_requests}
    from_account = await AccountRepository.create(json)
    to_account = await AccountRepository.create(json)

    tx_info = {"from_account_id": str(from_account["id"]), "to_account_id": str(to_account["id"]), "amount": 1000}

    requests = []
    for i in range(concurrent_requests):
        requests.append(new_client.post(url, json=tx_info))
    await asyncio.gather(*requests)

    from_account = await AccountRepository.get_by_id(from_account["id"])
    to_account = await AccountRepository.get_by_id(to_account["id"])
    assert from_account["amount"] == json["amount"] - tx_info["amount"] * concurrent_requests
    assert to_account["amount"] == json["amount"] + tx_info["amount"] * concurrent_requests
    assert from_account["version"] == expected_version
    assert to_account["version"] == expected_version


@mark.parametrize(
    "url, concurrent_deadlocks, expected_version",
    [
        ("/v1/accounts/transfer", 2, 0),
        ("/v2/accounts/transfer_isolation_level", 2, 0),
        ("/v2/accounts/transfer_optimistic_locking", 2, 4),
    ],
)
async def test_transfer_success_in_deadlock_scenario(new_client, url, concurrent_deadlocks, expected_version):
    user = await UserRepository.create({"email": "user@example.com", "password": "123456"})
    asset = await AssetRepository.create({"code": "example", "name": "example"})

    json = {"user_id": str(user["id"]), "asset_id": str(asset["id"]), "amount": 1000 * concurrent_deadlocks}
    from_account = await AccountRepository.create(json)
    to_account = await AccountRepository.create(json)

    tx_info1 = {"from_account_id": str(from_account["id"]), "to_account_id": str(to_account["id"]), "amount": 1000}
    tx_info2 = {"from_account_id": str(to_account["id"]), "to_account_id": str(from_account["id"]), "amount": 1000}
    requests = []
    for i in range(concurrent_deadlocks):
        requests.extend(
            [
                new_client.post(url, json=tx_info1),
                new_client.post(url, json=tx_info2),
            ]
        )
    await asyncio.gather(*requests)

    from_account = await AccountRepository.get_by_id(from_account["id"])
    to_account = await AccountRepository.get_by_id(to_account["id"])
    assert from_account["amount"] == json["amount"]
    assert to_account["amount"] == json["amount"]
    assert from_account["version"] == expected_version
    assert to_account["version"] == expected_version


@mark.parametrize(
    "url",
    [
        "/v1/accounts/transfer",
        "/v2/accounts/transfer_isolation_level",
        "/v2/accounts/transfer_optimistic_locking",
    ],
)
async def test_transfer_account_not_enough_balance(new_client, url):
    user = await UserRepository.create({"email": "user@example.com", "password": "123456"})
    asset = await AssetRepository.create({"code": "example", "name": "example"})

    json = {"user_id": str(user["id"]), "asset_id": str(asset["id"]), "amount": 0}
    from_account = await AccountRepository.create(json)
    to_account = await AccountRepository.create(json)

    tx_info = {"from_account_id": str(from_account["id"]), "to_account_id": str(to_account["id"]), "amount": 1000}
    res = await new_client.post(url, json=tx_info)
    assert res.status_code == status.HTTP_400_BAD_REQUEST

    _, message = parse_response_body(res)
    assert message == "Account doesn't have enough funds. Amount: {amount}, Transfer amount: {transfer_amount}".format(
        amount=int(from_account["amount"]), transfer_amount=tx_info["amount"]
    )


@mark.parametrize(
    "url",
    [
        "/v1/accounts/transfer",
        "/v2/accounts/transfer_isolation_level",
        "/v2/accounts/transfer_optimistic_locking",
    ],
)
async def test_transfer_different_asset_account(new_client, url):
    user = await UserRepository.create({"email": "user@example.com", "password": "123456"})

    asset1 = await AssetRepository.create({"code": "asset1", "name": "asset1"})
    json = {"user_id": str(user["id"]), "asset_id": str(asset1["id"]), "amount": 1000}
    from_account = await AccountRepository.create(json)

    asset2 = await AssetRepository.create({"code": "asset2", "name": "asset2"})
    json = {"user_id": str(user["id"]), "asset_id": str(asset2["id"]), "amount": 1000}
    to_account = await AccountRepository.create(json)

    tx_info = {"from_account_id": str(from_account["id"]), "to_account_id": str(to_account["id"]), "amount": 1000}
    res = await new_client.post(url, json=tx_info)
    assert res.status_code == status.HTTP_400_BAD_REQUEST

    _, message = parse_response_body(res)
    assert message == "Cannot transfer to a different asset account."
