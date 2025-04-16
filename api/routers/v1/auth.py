from fastapi import APIRouter, HTTPException, status

from core.services import users_service
from core.utils import create_access_token
from api.schemas.auth import LoginResponse
from api.oauth2 import PasswordRequestFormAnnotated


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/new_token", response_model=LoginResponse)
async def login(form_data: PasswordRequestFormAnnotated):
    user = await users_service.get_user_by_login_credentials(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credentials is invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(user["id"])
    return {"access_token": access_token, "token_type": "bearer"}
