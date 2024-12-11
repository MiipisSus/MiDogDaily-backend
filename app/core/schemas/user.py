from sqlalchemy.orm import Session
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr

from app.core.models import User


class UserBase(BaseModel):
    username: str
    email: EmailStr
    nickname: str
    coin: float


class UserCreate(UserBase):
    password: str
    

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

