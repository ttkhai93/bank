from tests.utils import parse_response_body


def test_get_user(test_client):
    res = test_client.get("/users")
    data, _ = parse_response_body(res)
    users = data.get("users")

    assert len(users) == 0


def test_create_user(test_client):
    json = {"email": "user@example.com", "password": "123456"}
    res = test_client.post("/users", json=json)
    data, _ = parse_response_body(res)
    user = data.get("user")

    assert json["email"] == user["email"]
    assert json["password"] == user["password"]


def test_create_user_already_exists(test_client):
    json = {"email": "user@example.com", "password": "123456"}
    res = test_client.post("/users", json=json)
    data, _ = parse_response_body(res)

    json = {"email": "user@example.com", "password": "123456"}
    res = test_client.post("/users", json=json)
    _, message = parse_response_body(res)

    assert message == "Key (email)=(user@example.com) already exists."


def test_create_user_wrong_email_format(test_client):
    json = {"email": "wrong_email_format", "password": "123456"}
    res = test_client.post("/users", json=json)
    _, message = parse_response_body(res)

    assert message.startswith("value is not a valid email address")
