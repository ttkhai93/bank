import os
from contextlib import contextmanager, asynccontextmanager

from httpx import Response

from core.db import engine


@asynccontextmanager
async def ctx_engine(postgres_url):
    try:
        engine.create(postgres_url)
        yield
    finally:
        await engine.dispose()


@contextmanager
def working_directory(path):
    """Temporarily change the current working directory."""
    original_cwd = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(original_cwd)


def parse_response_body(response: Response) -> (dict, str):
    response_body = response.json()
    status = response_body.get("status")
    data = response_body.get("data")
    message = response_body.get("message")

    if response.status_code == 200:
        assert status == "success", "'status' field should be 'success'"
        assert data is not None, "'data' field is expected in the response body: {}".format(response_body)
    if response.status_code >= 400:
        assert status == "error", "'status' field should be 'error'"
        assert message is not None, "'message' field is expected in the response body: {}".format(response_body)
    return data, message
