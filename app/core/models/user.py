from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from passlib.context import CryptContext
from typing import TYPE_CHECKING, Optional
from enum import IntEnum

if TYPE_CHECKING:
    from .task import Task, Tag


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Role(IntEnum):
    ADMIN = 1
    SUPERUSER = 2
    USER = 3


class UserBase(SQLModel):
    username: str = Field(unique=True)
    email: EmailStr = Field(unique=True, index=True)
    nickname: Optional[str] = Field(nullable=True, default=None)
    
    
class User(UserBase, table=True):
    __tablename__ = 'users'
    
    id : int = Field(primary_key=True, index=True)
    role_id: int = Field(foreign_key='user_roles.id', default=Role.USER)
    
    password: str
    
    coin: float = Field(default=0, nullable=True)
    
    role: 'UserRole' = Relationship(back_populates='users')
    tasks: list['Task'] = Relationship(back_populates='user')
    tags: list['Tag'] = Relationship(back_populates='owner')
    
    headshot_filepath: str = Field(nullable=True, default=None)
    
    def encode_password(self):        
        self.password = pwd_context.hash(self.password)
        
    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.password)
    

class UserRole(SQLModel, table=True):
    """
    若有新增新角色，記得在 Role 類別新增新的鍵值
    """
    __tablename__ = 'user_roles'
    
    id: int = Field(primary_key=True, index=True)
    name: str
    
    users: list['User'] = Relationship(back_populates='role')