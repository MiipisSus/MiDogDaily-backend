from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from app.core.models import Tag, User, Role
from app.core.schemas import TagCreate
from .utils import update_instance, validate_user_access


class TagService:
    @staticmethod
    def is_tag_exist(db: Session, id: int) -> Tag:
        tag = db.query(Tag).filter(Tag.id == id).first()
        if not tag:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Tag with id {id} does not exist')

        return tag
    
    @staticmethod
    def list_tags(db: Session, user: User) -> Page[Tag]:
        public_tags = db.query(Tag).filter(Tag.is_public == True)
        user_tags = db.query(Tag).join(User.tags).filter(User.id == user.id)
        tags = public_tags.union(user_tags).order_by(Tag.id)
        
        return paginate(tags)
    
    @staticmethod
    def create_tag(db: Session, user: User, data: TagCreate):
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
    
    @staticmethod
    def update_tag(db: Session, user: User, id: int, data: TagCreate):
        tag = TagService.is_tag_exist(db, id)
        validate_user_access(user, tag.owner_id)
        
        update_instance(tag, data)
        
        db.commit()
        db.refresh(tag)
        
        return tag
    
    @staticmethod
    def delete_tag(db: Session, user: User, id: int):
        tag = TagService.is_tag_exist(db, id)
        validate_user_access(user, tag.owner_id)
        
        db.delete(tag)
        db.commit()
        
        return