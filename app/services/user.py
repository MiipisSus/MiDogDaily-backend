from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from uuid import uuid4
import os

from app.core.config import settings
from app.core.models import User
from app.core.schemas import UserCreate, AdminUserCreate, UserPasswordUpdate
from .utils import update_instance, validate_user_access


HEADSHOT_PATH = settings.HEADSHOT_PATH


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
        
        INVALID_IMAGE_TYPE = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="圖片格式不正確"
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
    def list_users(cls, db: Session, role_id: Optional[int]) -> Page[User]:
        """列出除當前用戶外的所有用戶"""
        if role_id:
            query = db.query(User).filter(User.role_id == role_id)
        else:
            query = db.query(User).filter()
        return paginate(query)
    
    @classmethod
    def get_user(cls, db: Session, cur_user: User, id: int = None) -> User:
        """獲取特定用戶，並驗證訪問權限"""
        if id:
            user = cls.get_user_by_id(db, id)
        else:
            user = cur_user
        return user
    
    @classmethod
    def create_user(cls, db: Session, data: UserCreate | AdminUserCreate) -> User:
        """創建新用戶"""
        cls.validate_unique_fields(db, data)
    
        new_user = User(**data.model_dump())
            
        new_user.encode_password()
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    @classmethod
    def update_user(cls, db: Session, cur_user: User, data: UserCreate, id: int = None) -> User:
        """更新用戶資訊"""
        if id:
            user = cls.get_user_by_id(db, id)
        else:
            user = cur_user
        
        cls.validate_unique_fields(db, data, user)
        
        update_instance(user, data)
        db.commit()
        db.refresh(user)
        return user
    
    @classmethod
    def update_user_password(cls, db: Session, cur_user: User, data: UserPasswordUpdate):
        user = cur_user
        
        # 更新密碼
        user.password = data.password
        user.encode_password()
        
        db.commit()
        db.refresh(user)
        return user
    
    @classmethod
    def delete_user(cls, db: Session, cur_user: User, id: int = None) -> None:
        """刪除用戶"""
        if id:
            user = cls.get_user_by_id(db, id)
        else:
            user = cur_user
        
        db.delete(user)
        db.commit()
    
    @classmethod
    def upload_headshot(cls, db: Session, cur_user: User, file: UploadFile):
        user = cur_user
        
        if not file.content_type.startswith('image/'):
            raise cls.Exceptions.INVALID_IMAGE_TYPE
        
        file_ext = file.filename.split('.')[-1]
        filename = f"{uuid4()}.{file_ext}"
        
        upload_dir = os.path.join(HEADSHOT_PATH, f'{id}/')
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, filename)
        
        with open(file_path, 'wb') as buffer:
            buffer.write(file.file.read())
            
        if user.headshot_filepath and os.path.exists(user.headshot_filepath):
            os.remove(user.headshot_filepath)
            
        user.headshot_filepath = file_path
        db.commit()
        db.refresh(user)
        
        return {'filepath': user.headshot_filepath}
    
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