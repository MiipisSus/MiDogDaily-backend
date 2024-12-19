from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

from app.deps import SessionDEP
from app.services import AuthService


router = APIRouter()


@router.post('/login/')
def login(auth: Annotated[OAuth2PasswordRequestForm, Depends()], db: SessionDEP):
    return AuthService.login(db, auth)