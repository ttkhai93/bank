from typing import Annotated

from fastapi import Query

from core.services import UserService
from api import StandardAPIRouter
from api.schemas import CommonQueryParams
from api.schemas.users import CreateUserRequest, CreateUserResponse

router = StandardAPIRouter(prefix="/users", tags=["Users"])
user_service = UserService()


@router.get("/")
async def get_users(query: Annotated[CommonQueryParams, Query()]):
    users = await user_service.get_users(**query.model_dump())
    return {"users": users}


@router.post("/")
async def create_user(body: CreateUserRequest):
    user = await user_service.create_user(body.model_dump())
    return {"user": CreateUserResponse(email=user["email"])}
