import os
import contextlib


@contextlib.contextmanager
def working_directory(path):
    """Temporarily change the current working directory."""
    original_cwd = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(original_cwd)


def get_response_data(response) -> dict:
    assert response.status_code == 200
    response_body = response.json()
    data = response_body["data"]
    return data
