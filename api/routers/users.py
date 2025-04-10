from typing import Annotated

from fastapi import APIRouter, Query

from core.services import UserService
from ..schemas import CommonQueryParams

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
async def get_users(query: Annotated[CommonQueryParams, Query()]):
    return await UserService.get_users(**query.model_dump())
