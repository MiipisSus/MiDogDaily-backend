from typing import Optional

from app.core.models import TagBase


class TagCreate(TagBase):
    pass

class TagResponse(TagBase):
    id: int
    is_public: bool
    
    class Config:
        from_attributes = True