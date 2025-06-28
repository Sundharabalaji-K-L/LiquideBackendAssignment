from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserRegister(UserBase):
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserDto(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

