from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestFormStrict

from src.exceptions import UnauthorizedError
from src.api.security.jwt import verify_access_token
from src.api.schemas.auth import AuthenticatedUser


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/new_token", auto_error=False)


def get_current_user(access_token: Annotated[str, Depends(oauth2_scheme)]):
    if not access_token:
        raise UnauthorizedError("Please include a valid 'Authorization: Bearer <token>' header in your request.")

    payload = verify_access_token(access_token)
    return AuthenticatedUser(id=payload["sub"])


AuthenticatedUserAnnotated = Annotated[AuthenticatedUser, Depends(get_current_user)]
PasswordRequestFormAnnotated = Annotated[OAuth2PasswordRequestFormStrict, Depends()]
