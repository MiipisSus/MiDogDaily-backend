from typing import Optional

from app.core.models import UserBase, Role, UserRole
from .tasks import TaskResponse
from .tag import TagResponse

    
class UserCreate(UserBase):
    password: str
    

class AdminUserCreate(UserBase):
    password: str
    role_id: Role
    
class UserResponse(UserBase):
    id: int
    role: 'UserRole'
    coin: float
    tasks: list['TaskResponse']
    tags: list['TagResponse']
    
    class Config:
        from_attributes = True

