from pytest import mark
from fastapi import status

from tests.utils import parse_response_body
from src.domain.repositories import users_repo


@mark.parametrize(
    "url, expected_users, first_user",
    [
        ("/v1/users", 3, "user0@example.com"),
        ("/v1/users?offset=1&limit=2", 2, "user1@example.com"),
        ("/v1/users?order_by=email", 3, "user0@example.com"),
        ("/v1/users?order_by=-email", 3, "user2@example.com"),
    ],
)
async def test_get_user(new_client, url, expected_users, first_user):
    await users_repo.create_many([{"email": f"user{i}@example.com", "password": "123456"} for i in range(3)])

    res = await new_client.get(url)
    assert res.status_code == status.HTTP_200_OK

    data, _ = parse_response_body(res)
    users = data.get("users")
    assert len(users) == expected_users
    assert users[0]["email"] == first_user


async def test_create_user(new_client):
    json = {"email": "user@example.com", "password": "123456"}
    res = await new_client.post("/v1/users", json=json)
    assert res.status_code == status.HTTP_200_OK

    data, _ = parse_response_body(res)
    user = data.get("user")
    assert json["email"] == user["email"]


async def test_create_user_already_exists(new_client):
    json = {"email": "user@example.com", "password": "123456"}
    res = await new_client.post("/v1/users", json=json)
    data, _ = parse_response_body(res)

    json = {"email": "user@example.com", "password": "123456"}
    res = await new_client.post("/v1/users", json=json)
    assert res.status_code == status.HTTP_400_BAD_REQUEST

    _, message = parse_response_body(res)
    assert message == "Key (email)=(user@example.com) already exists."


async def test_create_user_wrong_email_format(new_client):
    json = {"email": "wrong_email_format", "password": "123456"}
    res = await new_client.post("/v1/users", json=json)
    assert res.status_code == status.HTTP_400_BAD_REQUEST

    _, message = parse_response_body(res)
    assert message.startswith("value is not a valid email address")


async def test_get_user_info_no_authorization_header_fail(new_client):
    res = await new_client.get("/v1/users/me")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

    _, message = parse_response_body(res)
    assert message == "Please include a valid 'Authorization: Bearer <token>' header in your request."


async def test_get_user_info_invalid_access_token_fail(new_client):
    res = await new_client.get("/v1/users/me", headers={"Authorization": "Bearer " + "invalid_token"})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

    _, message = parse_response_body(res)
    assert message == "Invalid access token"
