from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi_pagination import Page
from typing import List, Optional

from app.core.schemas import UserCreate, UserResponse
from app.core.models import get_db, User
from app.services import UserService

router = APIRouter()


@router.get('/', response_model=Page[UserResponse])
def get_user(db: Session = Depends(get_db)):
    return UserService.get_users(db)

@router.post('/', response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(db, user)

@router.put('/{id}', response_model=UserResponse)
def update_user(id: int, user: UserCreate, db: Session = Depends(get_db)):
    update_user = UserService