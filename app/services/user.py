from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from app.core.models import User
from app.core.schemas import UserCreate, AdminUserCreate

from .utils import update_instance, validate_user_access


class UserService:
    @staticmethod
    def validate_unique_fields(db: Session, data: UserCreate):
        UserService.validate_username_field(db, data)
        UserService.validate_email_field(db, data)
    
    @staticmethod
    def validate_username_field(db: Session, data: UserCreate):
        if db.query(User).filter(User.username == data.username).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="該帳號名稱已存在")
        
    @staticmethod
    def validate_email_field(db: Session, data: UserCreate):
        if db.query(User).filter(User.email == data.email).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="該電子郵件地址已存在")
        
    @staticmethod
    def is_user_exist(db: Session, id: int):
        user = db.query(User).filter(User.id == id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} does not exist')
        
        return user
    
    @staticmethod
    def list_users(db: Session, user: User) -> Page[User]:
        return paginate(db.query(User).filter(User.id != user.id))
    
    @staticmethod
    def get_user(db: Session, user: User, id: int) -> User:
        UserService.is_user_exist(db, id)
        validate_user_access(user, id)
        
        return user
        
    @staticmethod
    def create_user(db: Session, data: UserCreate) -> User:
        UserService.validate_unique_fields(db, data)
        
        new_user = User(
            **data.model_dump(),
            role_id=3
        )
        new_user.encode_password()
        
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
    
    @staticmethod
    def update_user(db: Session, user: User, id: int, data: UserCreate) -> User:
        UserService.is_user_exist(db, id)
        if user.username != data.username:
            UserService.validate_username_field(db, data)
        if user.email != data.email:
            UserService.validate_email_field(db, data)
        
        validate_user_access(user, id)
        
        update_instance(user, data)
            
        db.commit()
        db.refresh(user)
        
        return user
        
    @staticmethod
    def delete_user(db: Session, user: User, id: int):
        UserService.is_user_exist(db, id)
        validate_user_access(user, id)
        
        db.delete(user)
        db.commit()
        
        return
    
    @staticmethod
    def create_admin(db: Session, data: AdminUserCreate) -> User:
        UserService.validate_unique_fields(db, data)
        
        new_user = User(
            **data.model_dump()
        )
        new_user.encode_password()
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
    
    @staticmethod
    def update_admin(db: Session, id: int, data: AdminUserCreate) -> User:
        user = UserService.is_user_exist(db, id)
        if user.username != data.username:
            UserService.validate_username_field(db, data)
        if user.email != data.email:
            UserService.validate_email_field(db, data)
        
        update_instance(user, data)
        
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def delete_admin(db: Session, id: int):
        user = UserService.is_user_exist(db, id)
        
        db.delete(user)
        db.commit()
        
        return