from typing import Annotated

from fastapi import Query

from core.services import UserService
from api import StandardAPIRouter
from api.schemas import CommonQueryParams
from api.schemas.users import CreateUserRequest, CreateUserResponse
from api.routers.auth import AuthenticatedUserAnnotated


router = StandardAPIRouter(prefix="/users", tags=["Users"])
user_service = UserService()


@router.get("/me")
async def get_user_info(auth_user: AuthenticatedUserAnnotated):
    return {"user_id": auth_user.id}


@router.get("")
async def get_users(query: Annotated[CommonQueryParams, Query()]):
    users = await user_service.get_users(**query.model_dump())
    return {"users": users}


@router.post("")
async def create_user(body: CreateUserRequest):
    user = await user_service.create_user(body.model_dump())
    return {"user": CreateUserResponse(**user)}
