from fastapi import status

from tests.utils import parse_response_body


async def test_get_asset(new_client):
    res = await new_client.get("/v1/assets")
    assert res.status_code == status.HTTP_200_OK

    data, _ = parse_response_body(res)
    assets = data.get("assets")
    assert len(assets) == 0


async def test_create_asset(new_client):
    json = {"code": "example", "name": "example"}
    res = await new_client.post("/v1/assets", json=json)
    assert res.status_code == status.HTTP_200_OK

    data, _ = parse_response_body(res)
    asset = data.get("asset")
    assert json["code"] == asset["code"]
    assert json["name"] == asset["name"]


async def test_create_asset_already_exists(new_client):
    json = {"code": "example", "name": "example"}
    res = await new_client.post("/v1/assets", json=json)
    data, _ = parse_response_body(res)

    json = {"code": "example", "name": "example"}
    res = await new_client.post("/v1/assets", json=json)
    assert res.status_code == status.HTTP_400_BAD_REQUEST

    _, message = parse_response_body(res)
    assert message == "Key (code)=(example) already exists."
