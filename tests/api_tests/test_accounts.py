import asyncio

import pytest

from core.repositories import UserRepository, AssetRepository, AccountRepository
from tests.utils import parse_response_body


async def test_get_account(new_client):
    res = await new_client.get("/accounts")
    data, _ = parse_response_body(res)
    accounts = data.get("accounts")

    assert len(accounts) == 0


async def test_create_account(new_client):
    user = await UserRepository.create({"email": "user@example.com", "password": "123456"})
    asset = await AssetRepository.create({"code": "example", "name": "example"})

    json = {"user_id": str(user["id"]), "asset_id": str(asset["id"]), "amount": 1000}
    res = await new_client.post("/accounts", json=json)
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
    res = await new_client.post("/accounts/transfer", json=tx_info)
    data, _ = parse_response_body(res)
    transaction = data.get("transaction")

    from_account = await AccountRepository.get_by_id(from_account["id"])
    to_account = await AccountRepository.get_by_id(to_account["id"])

    assert transaction["from_account_id"] == tx_info["from_account_id"]
    assert transaction["to_account_id"] == tx_info["to_account_id"]
    assert transaction["amount"] == tx_info["amount"]
    assert transaction["status"] == "pending"

    assert from_account["amount"] == json["amount"] - tx_info["amount"]
    assert to_account["amount"] == json["amount"] + tx_info["amount"]


@pytest.mark.parametrize("concurrent_requests", [1000])
async def test_transfer_success_in_lost_update_scenario(new_client, concurrent_requests):
    user = await UserRepository.create({"email": "user@example.com", "password": "123456"})
    asset = await AssetRepository.create({"code": "example", "name": "example"})

    json = {"user_id": str(user["id"]), "asset_id": str(asset["id"]), "amount": 1000 * concurrent_requests}
    from_account = await AccountRepository.create(json)
    to_account = await AccountRepository.create(json)

    tx_info = {"from_account_id": str(from_account["id"]), "to_account_id": str(to_account["id"]), "amount": 1000}

    requests = []
    for i in range(concurrent_requests):
        requests.append(new_client.post("/accounts/transfer", json=tx_info))
    await asyncio.gather(*requests)

    from_account = await AccountRepository.get_by_id(from_account["id"])
    to_account = await AccountRepository.get_by_id(to_account["id"])

    assert from_account["amount"] == json["amount"] - tx_info["amount"] * concurrent_requests
    assert to_account["amount"] == json["amount"] + tx_info["amount"] * concurrent_requests


@pytest.mark.parametrize("concurrent_requests", [4])
async def test_transfer_success_in_lost_update_scenario_use_isolation_level(new_client, concurrent_requests):
    user = await UserRepository.create({"email": "user@example.com", "password": "123456"})
    asset = await AssetRepository.create({"code": "example", "name": "example"})

    json = {"user_id": str(user["id"]), "asset_id": str(asset["id"]), "amount": 1000 * concurrent_requests}
    from_account = await AccountRepository.create(json)
    to_account = await AccountRepository.create(json)

    tx_info = {"from_account_id": str(from_account["id"]), "to_account_id": str(to_account["id"]), "amount": 1000}
    requests = []
    for i in range(concurrent_requests):
        requests.append(new_client.post("/accounts/transfer_isolation_level", json=tx_info))
    await asyncio.gather(*requests)

    from_account = await AccountRepository.get_by_id(from_account["id"])
    to_account = await AccountRepository.get_by_id(to_account["id"])

    assert from_account["amount"] == json["amount"] - tx_info["amount"] * concurrent_requests
    assert to_account["amount"] == json["amount"] + tx_info["amount"] * concurrent_requests


@pytest.mark.parametrize("concurrent_requests", [4])
async def test_transfer_success_in_lost_update_scenario_use_optimistic_locking(new_client, concurrent_requests):
    user = await UserRepository.create({"email": "user@example.com", "password": "123456"})
    asset = await AssetRepository.create({"code": "example", "name": "example"})

    json = {"user_id": str(user["id"]), "asset_id": str(asset["id"]), "amount": 1000 * concurrent_requests}
    from_account = await AccountRepository.create(json)
    to_account = await AccountRepository.create(json)

    tx_info = {"from_account_id": str(from_account["id"]), "to_account_id": str(to_account["id"]), "amount": 1000}
    requests = []
    for i in range(concurrent_requests):
        requests.append(new_client.post("/accounts/transfer_optimistic_locking", json=tx_info))
    await asyncio.gather(*requests)

    from_account = await AccountRepository.get_by_id(from_account["id"])
    to_account = await AccountRepository.get_by_id(to_account["id"])

    assert from_account["amount"] == json["amount"] - tx_info["amount"] * concurrent_requests
    assert to_account["amount"] == json["amount"] + tx_info["amount"] * concurrent_requests
    assert from_account["version"] == concurrent_requests
    assert to_account["version"] == concurrent_requests


@pytest.mark.parametrize("concurrent_deadlocks", [2])
async def test_transfer_success_in_deadlock_scenario(new_client, concurrent_deadlocks):
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
                new_client.post("/accounts/transfer", json=tx_info1),
                new_client.post("/accounts/transfer", json=tx_info2),
            ]
        )
    await asyncio.gather(*requests)

    from_account = await AccountRepository.get_by_id(from_account["id"])
    to_account = await AccountRepository.get_by_id(to_account["id"])

    assert from_account["amount"] == json["amount"]
    assert to_account["amount"] == json["amount"]


@pytest.mark.parametrize("concurrent_deadlocks", [2])
async def test_transfer_success_in_deadlock_scenario_use_isolation_level(new_client, concurrent_deadlocks):
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
                new_client.post("/accounts/transfer_isolation_level", json=tx_info1),
                new_client.post("/accounts/transfer_isolation_level", json=tx_info2),
            ]
        )
    await asyncio.gather(*requests)

    from_account = await AccountRepository.get_by_id(from_account["id"])
    to_account = await AccountRepository.get_by_id(to_account["id"])

    assert from_account["amount"] == json["amount"]
    assert to_account["amount"] == json["amount"]


@pytest.mark.parametrize("concurrent_deadlocks", [2])
async def test_transfer_success_in_deadlock_scenario_use_optimistic_locking(new_client, concurrent_deadlocks):
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
                new_client.post("/accounts/transfer_optimistic_locking", json=tx_info1),
                new_client.post("/accounts/transfer_optimistic_locking", json=tx_info2),
            ]
        )
    await asyncio.gather(*requests)

    from_account = await AccountRepository.get_by_id(from_account["id"])
    to_account = await AccountRepository.get_by_id(to_account["id"])

    assert from_account["amount"] == json["amount"]
    assert to_account["amount"] == json["amount"]
    assert from_account["version"] == 2 * concurrent_deadlocks
    assert to_account["version"] == 2 * concurrent_deadlocks


async def test_transfer_not_enough_funds(new_client):
    user = await UserRepository.create({"email": "user@example.com", "password": "123456"})
    asset = await AssetRepository.create({"code": "example", "name": "example"})

    json = {"user_id": str(user["id"]), "asset_id": str(asset["id"]), "amount": 0}
    from_account = await AccountRepository.create(json)
    to_account = await AccountRepository.create(json)

    tx_info = {"from_account_id": str(from_account["id"]), "to_account_id": str(to_account["id"]), "amount": 1000}
    res = await new_client.post("/accounts/transfer", json=tx_info)
    _, message = parse_response_body(res)

    assert message == "Account doesn't have enough funds. Amount: {amount}, Transfer amount: {transfer_amount}".format(
        amount=int(from_account["amount"]), transfer_amount=tx_info["amount"]
    )


async def test_transfer_different_asset_account(new_client):
    user = await UserRepository.create({"email": "user@example.com", "password": "123456"})

    asset1 = await AssetRepository.create({"code": "asset1", "name": "asset1"})
    json = {"user_id": str(user["id"]), "asset_id": str(asset1["id"]), "amount": 1000}
    from_account = await AccountRepository.create(json)

    asset2 = await AssetRepository.create({"code": "asset2", "name": "asset2"})
    json = {"user_id": str(user["id"]), "asset_id": str(asset2["id"]), "amount": 1000}
    to_account = await AccountRepository.create(json)

    tx_info = {"from_account_id": str(from_account["id"]), "to_account_id": str(to_account["id"]), "amount": 1000}
    res = await new_client.post("/accounts/transfer", json=tx_info)
    _, message = parse_response_body(res)

    assert message == "Cannot transfer to a different asset account."
