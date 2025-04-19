from fastapi import APIRouter, HTTPException, status

from src.domain.services import users_service
from src.api.security.jwt import create_access_token
from src.api.schemas.auth import LoginResponse
from src.api.security.oauth2 import PasswordRequestFormAnnotated
from src.api.security.password import check_password


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/new_token", response_model=LoginResponse)
async def login(form_data: PasswordRequestFormAnnotated):
    users = await users_service.get_users(email=form_data.username)
    if not users or not check_password(form_data.password, users[0]["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credentials is invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(users[0]["id"])
    return {"access_token": access_token, "token_type": "bearer"}
