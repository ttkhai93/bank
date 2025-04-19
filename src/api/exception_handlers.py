from fastapi import Request
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError

from src.errors import ClientError
from .json_response import standardize_json_response


async def client_error_handler(_: Request, exc: ClientError):
    body = {"status": "error", "message": exc.message}
    return standardize_json_response(body=body, status_code=exc.status_code)


async def validation_exception_handler(_, exc: RequestValidationError):
    errors = exc.errors()
    body = {"status": "error", "message": errors[0]["msg"]}
    return standardize_json_response(body=body, status_code=400)


async def integrity_exception_handler(_, exc: IntegrityError):
    error_detail = str(exc.orig).split("DETAIL:")[1].replace('"', "'")
    message = error_detail.strip()
    body = {"status": "error", "message": message}
    return standardize_json_response(body=body, status_code=400)


exception_handlers = {
    ClientError: client_error_handler,
    RequestValidationError: validation_exception_handler,
    IntegrityError: integrity_exception_handler,
}
