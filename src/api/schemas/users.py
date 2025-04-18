from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str


class CreateUserResponse(BaseModel):
    id: UUID
    email: EmailStr
    created: datetime
    updated: datetime
    archived: bool
