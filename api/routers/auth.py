from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestFormStrict

from core.errors import ClientError
from core.services import UserService
from core.utils import create_access_token, verify_access_token
from api.schemas.auth import LoginResponse, AuthenticatedUser


router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/new_token")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user_id = verify_access_token(token)
    if not user_id:
        raise ClientError("Access token is invalid")

    return AuthenticatedUser(id=user_id)


@router.post("/new_token", response_model=LoginResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestFormStrict, Depends()]):
    user = await UserService().get_user_by_login_credentials(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credentials is invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(user["id"])
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def get_user_info(auth_user: Annotated[AuthenticatedUser, Depends(get_current_user)]):
    return {"user_id": auth_user.id}
