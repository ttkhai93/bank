from fastapi import Request

from core.errors import ClientError
from .json_response import standardize_json_response


async def client_error_handler(_: Request, exc: ClientError):
    body = {"status": "error", "message": exc.message}
    return standardize_json_response(body=body, status_code=exc.status_code)


exception_handlers = [
    (ClientError, client_error_handler),
]
