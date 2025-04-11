from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str


class CreateUserResponse(BaseModel):
    email: EmailStr
