from typing import Annotated

from fastapi import Query

from src.domain.services import users_service
from src.api.routers.standard_router import StandardAPIRouter
from src.api.schemas import CommonQueryParams
from src.api.schemas.users import CreateUserRequest, CreateUserResponse
from src.api.security.oauth2 import AuthenticatedUserAnnotated
from src.api.security.password import hash_password
from src.api.security.rate_limit import RateLimiter3PerSecond


router = StandardAPIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
async def get_user_info(auth_user: AuthenticatedUserAnnotated, limiter: RateLimiter3PerSecond):
    return {"user_id": auth_user.id}


@router.get("")
async def get_users(query: Annotated[CommonQueryParams, Query()]):
    users = await users_service.get_users(**query.model_dump())
    return {"users": users}


@router.post("")
async def create_user(body: CreateUserRequest):
    user_info = body.model_dump()
    user_info["password"] = hash_password(user_info["password"])

    user = await users_service.create_user(user_info)
    return {"user": CreateUserResponse(**user)}
