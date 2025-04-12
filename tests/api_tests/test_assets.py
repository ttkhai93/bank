from tests.utils import parse_response_body


def test_get_asset(test_client):
    res = test_client.get("/assets")
    data, _ = parse_response_body(res)
    assets = data.get("assets")

    assert len(assets) == 0


def test_create_asset(test_client):
    json = {"code": "example", "name": "example"}
    res = test_client.post("/assets", json=json)
    data, _ = parse_response_body(res)
    asset = data.get("asset")

    assert json["code"] == asset["code"]
    assert json["name"] == asset["name"]


def test_create_asset_already_exists(test_client):
    json = {"code": "example", "name": "example"}
    res = test_client.post("/assets", json=json)
    data, _ = parse_response_body(res)

    json = {"code": "example", "name": "example"}
    res = test_client.post("/assets", json=json)
    _, message = parse_response_body(res)

    assert message == "Key (code)=(example) already exists."
