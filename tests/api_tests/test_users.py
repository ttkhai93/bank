from tests.utils import parse_response_body


async def test_get_user(new_client):
    res = await new_client.get("/users")
    data, _ = parse_response_body(res)
    users = data.get("users")

    assert len(users) == 0


async def test_create_user(new_client):
    json = {"email": "user@example.com", "password": "123456"}
    res = await new_client.post("/users", json=json)
    data, _ = parse_response_body(res)
    user = data.get("user")

    assert json["email"] == user["email"]


async def test_create_user_already_exists(new_client):
    json = {"email": "user@example.com", "password": "123456"}
    res = await new_client.post("/users", json=json)
    data, _ = parse_response_body(res)

    json = {"email": "user@example.com", "password": "123456"}
    res = await new_client.post("/users", json=json)
    _, message = parse_response_body(res)

    assert message == "Key (email)=(user@example.com) already exists."


async def test_create_user_wrong_email_format(new_client):
    json = {"email": "wrong_email_format", "password": "123456"}
    res = await new_client.post("/users", json=json)
    _, message = parse_response_body(res)

    assert message.startswith("value is not a valid email address")


async def test_get_user_info_no_authorization_header_fail(new_client):
    res = await new_client.get("users/me")
    _, message = parse_response_body(res)
    assert message == "Please include a valid 'Authorization: Bearer <token>' header in your request."


async def test_get_user_info_invalid_access_token_fail(new_client):
    res = await new_client.get("users/me", headers={"Authorization": "Bearer " + "invalid_token"})
    _, message = parse_response_body(res)
    assert message == "Access token is invalid"
