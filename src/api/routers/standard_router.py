import json
from typing import Any, Literal

from fastapi import Request, Response
from fastapi.routing import APIRoute, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class JSONResponseBody(BaseModel):
    status: Literal["success", "error"]
    data: dict[str, Any] = None  # Required If status = "success"
    message: str = None  # Required If status = "error"

    def model_dump(self, **kwargs):
        return super().model_dump(exclude_unset=True)


class StandardAPIRoute(APIRoute):
    def get_route_handler(self):
        orig_get_request_handler = super().get_route_handler()

        async def get_request_handler(request: Request) -> Response:
            response = await orig_get_request_handler(request)
            data = json.loads(response.body)
            assert isinstance(data, dict), "Result data should be a dictionary"  # Don't depend on assert for validation

            if not data:
                data = {}

            content = JSONResponseBody(status="success", data=data).model_dump()
            return JSONResponse(status_code=response.status_code, content=content)

        return get_request_handler


class StandardAPIRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("route_class", StandardAPIRoute)
        super().__init__(*args, **kwargs)
