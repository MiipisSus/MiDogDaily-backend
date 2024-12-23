from fastapi import APIRouter, status, Query
from fastapi_pagination import Page
from typing import Optional

from app.core.schemas import UserCreate, AdminUserCreate, UserResponse
from app.core.models import Role
from app.services import UserService
from app.deps import SessionDEP, UserDEP, AdminDEP


router = APIRouter()


@router.get(
    '/{id:int}/',
    response_model=UserResponse,
    summary='獲取單一使用者的資料'
    )
def get_user(db: SessionDEP, user: UserDEP, id: int):
    return UserService.get_user(db, user, id)

@router.post(
    '/',
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary='創建一般使用者')
def create_user(db: SessionDEP, data: UserCreate):
    return UserService.create_user(db, data)

@router.put(
    '/{id:int}/',
    response_model=UserResponse,
    summary='更新一般或超級使用者的資料'
    )
def update_user(db: SessionDEP, user: UserDEP, id: int, data: UserCreate):
    return UserService.update_user(db, user, id, data)

@router.delete(
    '/{id:int}/',
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary='刪除一般或超級使用者'
    )
def delete_user(db: SessionDEP, user: UserDEP, id: int):
    return UserService.delete_user(db, user, id)

@router.get(
    '/admin/',
    response_model=Page[UserResponse],
    summary='（需要管理者權限）獲取所有使用者的資料'
    )
def list_users(
    db: SessionDEP,
    user: AdminDEP,
    role_id: Optional[Role] = Query(
        default=None,
        description='管理員=1, 超級使用者=2, 一般使用者=3'
        )
    ):
    return UserService.list_users(db, user)

@router.post(
    '/admin/',
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary='（需要管理者權限）創建一般使用者、超級使用者或管理員',
    description="""
    * **role_id** 管理員=1, 超級使用者=2, 一般使用者=3
    """
    )
def create_admin(db: SessionDEP, user: AdminDEP, data: AdminUserCreate):
    return UserService.create_admin(db, data)

@router.put(
    '/admin/{id:int}/',
    response_model=UserResponse,
    summary='（需要管理者權限）修改一般使用者、超級使用者或管理員',
)
def update_admin(db: SessionDEP, user: AdminDEP, id: int, data: AdminUserCreate):
    return UserService.update_admin(db, id, data)

@router.delete(
    '/admin/{id:int}/',
    status_code=status.HTTP_400_BAD_REQUEST,
    summary='（需要管理者權限）刪除一般使用者、超級使用者或管理員'
)
def delete_admin(db: SessionDEP, user: AdminDEP, id: int):
    return UserService.delete_admin(db, id)