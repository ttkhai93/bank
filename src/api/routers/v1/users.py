from typing import Annotated

from fastapi import Query

from src.domain.services import users_service
from src.api import StandardAPIRouter
from src.api.schemas import CommonQueryParams
from src.api.schemas.users import CreateUserRequest, CreateUserResponse
from src.api.security.oauth2 import AuthenticatedUserAnnotated


router = StandardAPIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
async def get_user_info(auth_user: AuthenticatedUserAnnotated):
    return {"user_id": auth_user.id}


@router.get("")
async def get_users(query: Annotated[CommonQueryParams, Query()]):
    users = await users_service.get_users(**query.model_dump())
    return {"users": users}


@router.post("")
async def create_user(body: CreateUserRequest):
    user = await users_service.create_user(body.model_dump())
    return {"user": CreateUserResponse(**user)}
