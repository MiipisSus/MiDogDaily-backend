from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional

from .task import TaskTagLink

if TYPE_CHECKING:
    from .user import User
    from .task import Task


class TagBase(SQLModel):
    name: str = Field(nullable=False)
    
    
class Tag(TagBase, table=True):
    __tablename__ = 'tags'
    
    id: int = Field(primary_key=True, index=True)
    owner_id: int = Field(foreign_key='users.id', ondelete='CASCADE')
    
    is_public: bool = Field(default=False, nullable=False)
    
    owner: 'User' = Relationship(back_populates='tags')
    tasks: list['Task'] = Relationship(back_populates='tags', link_model=TaskTagLink)