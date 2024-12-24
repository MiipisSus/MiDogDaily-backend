from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from app.core.models import User
from app.core.schemas import UserCreate, AdminUserCreate
from .utils import update_instance, validate_user_access

class UserService:
    """處理用戶相關的業務邏輯"""
    
    class Exceptions:
        """集中管理錯誤訊息"""
        USERNAME_EXISTS = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="該帳號名稱已存在"
        )
        EMAIL_EXISTS = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="該電子郵件地址已存在"
        )
        
        @staticmethod
        def user_not_found(id: int) -> HTTPException:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'User with id {id} does not exist'
            )
    
    @classmethod
    def _get_user_by_username(cls, db: Session, username: str) -> Optional[User]:
        """根據用戶名查詢用戶"""
        return db.query(User).filter(User.username == username).first()
    
    @classmethod
    def _get_user_by_email(cls, db: Session, email: str) -> Optional[User]:
        """根據電子郵件查詢用戶"""
        return db.query(User).filter(User.email == email).first()
    
    @classmethod
    def validate_unique_fields(cls, db: Session, data: UserCreate, user: User = None) -> None:
        """驗證用戶名和電子郵件的唯一性"""
        if user:
            # 檢查更新檔案，需排除原實例 ID
            if user.username != data.username and cls._get_user_by_username(db, data.username):
                raise cls.Exceptions.USERNAME_EXISTS
            if user.email != data.email and cls._get_user_by_email(db, data.email):
                raise cls.Exceptions.EMAIL_EXISTS
        else:
            # 檢查創建檔案
            if cls._get_user_by_username(db, data.username):
                raise cls.Exceptions.USERNAME_EXISTS
            if cls._get_user_by_email(db, data.email):
                raise cls.Exceptions.EMAIL_EXISTS
    
    @classmethod
    def get_user_by_id(cls, db: Session, id: int) -> User:
        """根據ID獲取用戶，如果不存在則拋出異常"""
        user = db.query(User).filter(User.id == id).first()
        if not user:
            raise cls.Exceptions.user_not_found(id)
        return user
    
    @classmethod
    def list_users(cls, db: Session, cur_user: User) -> Page[User]:
        """列出除當前用戶外的所有用戶"""
        query = db.query(User).filter(User.id != cur_user.id)
        return paginate(query)
    
    @classmethod
    def get_user(cls, db: Session, cur_user: User, id: int) -> User:
        """獲取特定用戶，並驗證訪問權限"""
        user = cls.get_user_by_id(db, id)
        validate_user_access(cur_user, id)
        return user
    
    @classmethod
    def create_user(cls, db: Session, data: UserCreate, role_id: int = 3) -> User:
        """創建新用戶"""
        cls.validate_unique_fields(db, data)
        
        new_user = User(**data.model_dump(), role_id=role_id)
        new_user.encode_password()
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    @classmethod
    def update_user(cls, db: Session, cur_user: User, id: int, data: UserCreate) -> User:
        """更新用戶資訊"""
        user = cls.get_user_by_id(db, id)
        validate_user_access(cur_user, id)
        
        cls.validate_unique_fields(db, data, user)
        
        update_instance(user, data)
        db.commit()
        db.refresh(user)
        return user
    
    @classmethod
    def delete_user(cls, db: Session, cur_user: User, id: int) -> None:
        """刪除用戶"""
        user = cls.get_user_by_id(db, id)
        validate_user_access(cur_user, id)
        
        db.delete(user)
        db.commit()
    
    @classmethod
    def create_admin(cls, db: Session, data: AdminUserCreate) -> User:
        """創建管理員用戶"""
        cls.validate_unique_fields(db, data)
        
        new_user = User(**data.model_dump())
        new_user.encode_password()
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user