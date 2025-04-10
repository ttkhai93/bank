from fastapi import Request
from fastapi.responses import JSONResponse

from core.errors import ClientError


async def client_error_handler(_: Request, exc: ClientError):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})


exception_handlers = [
    (ClientError, client_error_handler),
]
