import json
from typing import Any

from fastapi import APIRouter, Request, Response
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse

from .schemas import JSONResponseBody


def standardize_json_response(body: dict[str, Any], status_code: int = 200) -> JSONResponse:
    content = JSONResponseBody(**body).model_dump()
    return JSONResponse(status_code=status_code, content=content)


class StandardAPIRoute(APIRoute):
    def get_route_handler(self):
        orig_get_request_handler = super().get_route_handler()

        async def get_request_handler(request: Request) -> Response:
            response = await orig_get_request_handler(request)
            data = json.loads(response.body)
            assert isinstance(data, dict), "Result data should be a dictionary"  # Don't depend on assert for validation

            body = {"status": "success", "data": data or {}}
            return standardize_json_response(body=body, status_code=response.status_code)

        return get_request_handler


class StandardAPIRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("route_class", StandardAPIRoute)
        super().__init__(*args, **kwargs)
