from typing import Optional
from sqlmodel import SQLModel

from app.core.models import UserBase, Role, UserRole
from .task import TaskResponse
from .tag import TagResponse

    
class UserCreate(UserBase):
    password: str
    
class UserUpdate(UserBase):
    pass

class AdminUserCreate(UserBase):
    password: str
    role_id: Role
    
class UserPasswordUpdate(SQLModel):
    password: str
    
class UserResponse(UserBase):
    id: int
    role: 'UserRole'
    coin: float
    tasks: list['TaskResponse']
    tags: list['TagResponse']
    headshot_filepath: Optional[str]
    
    class Config:
        from_attributes = True
