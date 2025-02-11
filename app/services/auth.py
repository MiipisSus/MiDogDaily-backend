from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from datetime import datetime, timedelta

from app.core.config import settings
from app.core.models import get_db, User, Role
from app.core.schemas import AuthLogin


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

OAuth2 = OAuth2PasswordBearer(tokenUrl='/api/auth/token/')


class AuthService:
    @classmethod
    def create_access_token(cls, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update(exp=expire)
        access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        return access_token
    
    @classmethod
    def login(cls, db: Session, data: AuthLogin):
        user = db.query(User).filter(User.username == data.username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='該用戶不存在')
        
        if not user.verify_password(data.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='密碼不正確')
        
        access_token = cls.create_access_token(
            data={
                'sub': str(user.id),
                'role_id': user.role_id
            }
        )
        
        response = {
            'access_token': access_token,
            'token_type': 'bearer',
            'user': user
        }
        
        return response
    
    @classmethod
    def is_user(cls, db: Session = Depends(get_db), token: str = Depends(OAuth2)) -> User:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('sub')
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return user
        
    @classmethod
    def is_superuser(cls, db: Session = Depends(get_db), token: str = Depends(OAuth2)) -> User:
        user = cls.is_user(db, token)
        if user.role_id in (Role.SUPERUSER, Role.ADMIN):
            return user
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="使用者權限不足，無法進行此操作")
        
    @classmethod
    def is_admin(cls, db: Session = Depends(get_db), token: str = Depends(OAuth2)) -> User:
        user = cls.is_user(db, token)
        if user.role_id == Role.ADMIN:
            return user
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="使用者權限不足，無法進行此操作")