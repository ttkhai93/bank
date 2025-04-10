from typing import Annotated

from fastapi import Query

from core.services import UserService
from api import StandardAPIRouter
from api.schemas import CommonQueryParams

router = StandardAPIRouter(prefix="/users", tags=["Users"])


@router.get("/")
async def get_users(query: Annotated[CommonQueryParams, Query()]):
    users = await UserService.get_users(**query.model_dump())
    return {"users": users}
