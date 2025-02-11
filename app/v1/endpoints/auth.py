from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

from app.deps import SessionDEP, UserDEP
from app.services import AuthService
from app.core.schemas import AuthLogin, AuthLoginResponse

router = APIRouter()

@router.post(
    '/token/',
    summary='（Swagger UI 的 Authorize 功能專用）')
def token(auth: Annotated[OAuth2PasswordRequestForm, Depends()], db: SessionDEP):
    return AuthService.login(db, auth)

@router.post(
    '/login/',
    summary='使用者登入',
    response_model=AuthLoginResponse)
def login(data: AuthLogin, db: SessionDEP):
    return AuthService.login(db, data)