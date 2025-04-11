from typing import Annotated

from fastapi import Query

from core.services import UserService
from api import StandardAPIRouter
from api.schemas import CommonQueryParams
from api.schemas.users import CreateUser

router = StandardAPIRouter(prefix="/users", tags=["Users"])


@router.get("/")
async def get_users(query: Annotated[CommonQueryParams, Query()]):
    users = await UserService.get_users(**query.model_dump())
    return {"users": users}


@router.post("/")
async def create_user(body: CreateUser):
    user = await UserService.create_user(body.model_dump())
    return {"user": user}
