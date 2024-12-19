from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional
from enum import Enum
from datetime import datetime

if TYPE_CHECKING:
    from .user import User
    from .tag import Tag

class Difficulty(Enum):
    EASY = 'EASY'
    MEDIUM = 'MEDIUM'
    HARD = 'HARD'
    

class Priority(Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    
    
class TaskTagLink(SQLModel, table=True):
    __tablename__ = 'task_tag_link'
    
    task_id: int = Field(foreign_key='tasks.id', primary_key=True, ondelete='CASCADE')
    tag_id: int = Field(foreign_key='tags.id', primary_key=True, ondelete='CASCADE')


class TaskBase(SQLModel):
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    difficulty: Difficulty = Field(default=Difficulty.MEDIUM, nullable=False)
    priority: Priority =  Field(default=Priority.MEDIUM, nullable=False)
    deadline: Optional[datetime] = Field(nullable=True, default=None)


class Task(TaskBase, table=True):
    __tablename__ = 'tasks'
    
    id: int = Field(primary_key=True, index=True)
    user_id: int = Field(foreign_key='users.id', ondelete='CASCADE')
    
    create_at: datetime = Field(default_factory=datetime.now, nullable=False)
    
    user: 'User' = Relationship(back_populates='tasks')
    tags: list['Tag'] = Relationship(back_populates='tasks', link_model=TaskTagLink)


