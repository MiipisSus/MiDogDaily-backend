from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from datetime import datetime, timedelta

from app.core.config import settings
from app.core.models import get_db, User, Role


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

OAuth2 = OAuth2PasswordBearer(tokenUrl='/api/auth/login')


class AuthService:
    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update(exp=expire)
        access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        return access_token
    
    @staticmethod
    def login(db: Session, data: OAuth2PasswordRequestForm):
        user = db.query(User).filter(User.username == data.username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='該用戶不存在')
        
        if not user.verify_password(data.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='密碼不正確')
        
        access_token = AuthService.create_access_token(
            data={
                'sub': str(user.id),
                'role_id': user.role_id
            }
        )
        
        return {'access_token': access_token, 'token_type': 'bearer'}
    
    @staticmethod
    def is_user(db: Session = Depends(get_db), token: str = Depends(OAuth2)) -> User:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get('sub')
            if not user_id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

            return user
        except:
            raise HTTPException(status_code=401)
        
    @staticmethod
    def is_superuser(db: Session = Depends(get_db), token: str = Depends(OAuth2)) -> User:
        user = AuthService.is_user(db, token)
        if user.role_id in (Role.SUPERUSER, Role.ADMIN):
            return user
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="使用者權限不足，無法進行此操作")
        
    @staticmethod
    def is_admin(db: Session = Depends(get_db), token: str = Depends(OAuth2)) -> User:
        user = AuthService.is_user(db, token)
        if user.role_id == Role.ADMIN:
            return user
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="使用者權限不足，無法進行此操作")