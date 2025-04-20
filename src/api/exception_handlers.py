from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError

from src.exceptions import ClientError
from .routers.standard_router import JSONResponseBody


async def client_error_handler(_, exc: ClientError):
    content = JSONResponseBody(status="error", message=exc.message).model_dump()
    return JSONResponse(status_code=exc.status_code, content=content)


async def validation_exception_handler(_, exc: RequestValidationError):
    errors = exc.errors()
    content = JSONResponseBody(status="error", message=errors[0]["msg"]).model_dump()
    return JSONResponse(status_code=400, content=content)


async def integrity_exception_handler(_, exc: IntegrityError):
    error_detail = str(exc.orig).split("DETAIL:")[1].replace('"', "'")
    message = error_detail.strip()
    content = JSONResponseBody(status="error", message=message).model_dump()
    return JSONResponse(status_code=400, content=content)


exception_handlers = {
    ClientError: client_error_handler,
    RequestValidationError: validation_exception_handler,
    IntegrityError: integrity_exception_handler,
}
