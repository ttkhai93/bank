from fastapi import Request
from fastapi.responses import JSONResponse

from core.errors import ClientError
from .schemas import JSONResponseBody, JSONResponseBodyStatus


def standardize_error_response(message: str, status_code: int) -> JSONResponse:
    body = JSONResponseBody(message=message, status=JSONResponseBodyStatus.ERROR)
    content = body.model_dump(exclude_unset=True)
    return JSONResponse(status_code=status_code, content=content)


async def client_error_handler(_: Request, exc: ClientError):
    return standardize_error_response(exc.message, exc.status_code)


exception_handlers = [
    (ClientError, client_error_handler),
]
