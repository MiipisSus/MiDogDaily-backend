from datetime import datetime
from sqlmodel import Field, SQLModel

from app.core.models import TaskBase
from .tag import TagResponse


class TaskCreate(TaskBase):
    tag_ids: list[int] = Field()
    is_completed: bool = Field(default=False)
    
    
class TaskResponse(TaskBase):
    id: int
    user_id: int
    create_at: datetime
    is_completed: bool = Field(default=False)
    tags: list['TagResponse']