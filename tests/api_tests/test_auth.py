from fastapi import status

from ..utils import parse_response_body


async def test_oauth2_password_flow_success(new_client):
    user_info = {"email": "user@example.com", "password": "123456"}
    await new_client.post("/v1/users", json=user_info)

    form_data = {"grant_type": "password", "username": user_info["email"], "password": user_info["password"]}
    res = await new_client.post("/v1/auth/new_token", data=form_data)
    body = res.json()
    assert res.status_code == status.HTTP_200_OK
    assert body.get("access_token")
    assert body.get("token_type") == "bearer"

    res = await new_client.get("/v1/users/me", headers={"Authorization": "Bearer " + body.get("access_token")})
    assert res.status_code == status.HTTP_200_OK

    data, _ = parse_response_body(res)
    assert data["user_id"]


async def test_get_access_token_invalid_username_fail(new_client):
    user_info = {"email": "user@example.com", "password": "123456"}

    form_data = {"grant_type": "password", "username": user_info["email"], "password": user_info["password"]}
    res = await new_client.post("/v1/auth/new_token", data=form_data)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_access_token_invalid_password_fail(new_client):
    user_info = {"email": "user@example.com", "password": "123456"}
    await new_client.post("users", json=user_info)

    form_data = {"grant_type": "password", "username": user_info["email"], "password": "wrong password"}
    res = await new_client.post("/v1/auth/new_token", data=form_data)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_user_info_no_authorization_header_fail(new_client):
    res = await new_client.get("/v1/users/me")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_user_info_no_invalid_access_token_fail(new_client):
    res = await new_client.get("/v1/users/me", headers={"Authorization": "Bearer " + "invalid token"})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
