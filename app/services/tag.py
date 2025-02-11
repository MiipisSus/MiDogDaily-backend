from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from app.core.models import Tag, User, Role
from app.core.schemas import TagCreate
from .utils import update_instance, validate_user_access


class TagService:
    """處理標籤的業務邏輯"""
    
    class Exceptions:
        @staticmethod
        def tag_not_found(id: int) -> HTTPException:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Tag with id {id} does not exist'
            )
        
    @classmethod
    def _get_tag_by_id(cls, db: Session, id: int) -> Tag:
        tag = db.query(Tag).filter(Tag.id == id).first()
        if not tag:
            raise cls.Exceptions.tag_not_found(id)
            
        return tag
    
    @classmethod
    def list_tags(cls, db: Session, user: User, is_public) -> Page[Tag]:
        public_tags = db.query(Tag).filter(Tag.is_public == True)
        user_tags = db.query(Tag).join(User.tags).filter(User.id == user.id)
        if is_public:
            tags = public_tags.union(user_tags).order_by(Tag.id)
        else:
            tags = user_tags
        
        return paginate(tags)
    
    @classmethod
    def create_tag(cls, db: Session, user: User, data: TagCreate):
        new_tag = Tag(
            **data.model_dump(),
            owner_id=user.id
        )
        
        if user.role_id == Role.ADMIN:
            new_tag.is_public = True
            
        db.add(new_tag)
        db.commit()
        db.refresh(new_tag)
        
        return new_tag
    
    @classmethod
    def update_tag(cls, db: Session, user: User, id: int, data: TagCreate):
        tag = cls._get_tag_by_id(db, id)
        validate_user_access(user, tag.owner_id)
        
        update_instance(tag, data)
        
        db.commit()
        db.refresh(tag)
        
        return tag
    
    @classmethod
    def delete_tag(cls, db: Session, user: User, id: int):
        tag = cls._get_tag_by_id(db, id)
        validate_user_access(user, tag.owner_id)
        
        db.delete(tag)
        db.commit()
        
        return