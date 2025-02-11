from fastapi import APIRouter, status, Query, UploadFile, File
from fastapi_pagination import Page
from typing import Optional

from app.core.schemas import UserCreate, UserUpdate, UserResponse, UserPasswordUpdate, AdminUserCreate
from app.core.models import Role
from app.services import UserService
from app.deps import SessionDEP, UserDEP, AdminDEP


router = APIRouter()


@router.get(
    '/{id:int}/',
    response_model=UserResponse,
    summary='（需要管理者權限）獲取一般使用者、超級使用者或管理員的資料'
    )
def get_user(
    db: SessionDEP,
    user: AdminDEP,
    id: int):
    return UserService.get_user(db, user, id)

@router.get(
    '/',
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
    return UserService.list_users(db, role_id)

@router.post(
    '/',
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary='（需要管理者權限）創建一般使用者、超級使用者或管理員'
    )
def create_user(
    db: SessionDEP,
    user: AdminDEP,
    data: AdminUserCreate
    ):
    return UserService.create_admin(db, data)

@router.put(
    '/{id:int}/',
    response_model=UserResponse,
    summary='（需要管理者權限）更新一般使用者、超級使用者或管理員'
    )
def update_user(
    db: SessionDEP,
    user: AdminDEP,
    id: int,
    data: UserUpdate
    ):
    return UserService.update_user(db, user, data, id)

@router.delete(
    '/{id:int}/',
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary='（需要管理者權限）刪除一般使用者、超級使用者或管理員'
    )
def delete_user(db: SessionDEP, user: UserDEP, id: int):
    return UserService.delete_user(db, user, id)

@router.post(
    '/register/',
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary='註冊一般使用者')
def create_user(
    db: SessionDEP,
    data: UserCreate):
    return UserService.create_user(db, data)

@router.get(
    '/me/',
    response_model=UserResponse,
    summary='獲取使用者自己的資料')
def get_user_me(db: SessionDEP, user: UserDEP):
    return UserService.get_user(db, user)

@router.put(
    '/me/',
    response_model=UserResponse,
    summary='更新使用者自己的資料'
)
def update_user_me(db: SessionDEP, user: UserDEP, data: UserCreate):
    return UserService.update_user(db, user, data)

@router.put(
    '/password/me/',
    response_model=UserResponse,
    summary='重置使用者自己的密碼'
)
def update_user_password(db: SessionDEP, user: UserDEP, data: UserPasswordUpdate):
    return UserService.update_user_password(db, user, data)

@router.delete(
    '/me/',
    summary='刪除使用者自己的資料'
)
def delete_user_me(db: SessionDEP, user: UserDEP):
    return UserService.delete_user(db, user)
    
@router.post(
    '/headshot/me/',
    response_model=None,
    summary='上傳頭像')
def upload_headshot(db: SessionDEP, user: UserDEP, file: UploadFile = File(...)):
    return UserService.upload_headshot(db, user, file)