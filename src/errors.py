class ClientError(Exception):
    """Should be used for generic client errors"""

    status_code = 400

    def __init__(self, message: str):
        self.message = message


class UnauthorizedError(ClientError):
    status_code = 401
