from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from app.core.models import User
from app.core.schemas import UserCreate


class UserService:
    @staticmethod
    def validate_user(db: Session, user: UserCreate):
        if db.query(User).filter(User.username == user.username).first():
            raise HTTPException(status_code=400, detail="該帳號名稱已存在")
        if db.query(User).filter(User.email == user.email).first():
            raise HTTPException(status_code=400, detail="該電子郵件地址已存在")
    
    @staticmethod
    def get_single_user(db: Session, id: int):
        user = db.query(User).filter(User.id == id).first()
        if not user:
            raise HTTPException(status_code=400, detail='User not found')
        
        return user
    
    @staticmethod
    def get_users(db: Session) -> Page[User]:
        return paginate(db.query(User))
    
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        UserService.validate_user(db, user)
        
        new_user = User(
            **user.dict()
        )
        new_user.encode_password()
        
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
    
    @staticmethod
    def update_user(db: Session, id: int, data: UserCreate) -> User:
        user = UserService.get_single_user(db, id)
        
        for field, value in data.dict().items():
            setattr(user, field, value)
            
        db.commit()
        db.refresh(user)
        
        return user
        
    @staticmethod
    def delete_user(db: Session, id: int):
        user = UserService.get_single_user(db, id)
        
        db.delete(user)