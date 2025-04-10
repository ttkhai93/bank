from fastapi import APIRouter

from core.services import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
async def get_users():
    return await UserService.get_users()
