from tests.utils import get_response_data


def test_get_user(test_client):
    res = test_client.get("/users")
    data = get_response_data(res)
    users = data.get("users")

    assert len(users) == 0
