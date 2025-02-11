from datetime import datetime
from sqlmodel import Field

from app.core.models import TaskBase
from .tag import TagResponse


class TaskCreate(TaskBase):
    tag_ids: list[int]
    
    
class TaskResponse(TaskBase):
    id: int
    user_id: int
    create_at: datetime
    is_done: bool = Field(default=False)
    tags: list['TagResponse']
    
    class Config:
        from_attributes = True