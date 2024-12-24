from fastapi import APIRouter, status, Query
from fastapi_pagination import Page
from typing import Optional

from app.core.schemas import TaskCreate, TaskResponse
from app.services import TaskService
from app.deps import SessionDEP, UserDEP

router = APIRouter()

@router.get(
    '/',
    response_model=Page[TaskResponse],
    summary='獲取所有任務'
    )
def list_tasks(
    db: SessionDEP,
    user: UserDEP,
    user_id: int = Query(description='使用者的 ID')
    ):
    return TaskService.list_tasks(db, user, user_id)

@router.post(
    '/',
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary='創建新任務'
    )
def create_task(db: SessionDEP, user: UserDEP, data: TaskCreate):
    return TaskService.create_task(db, user, data)

@router.put(
    '/{id:int}/',
    response_model=TaskResponse,
    summary='更新現有任務'
    )
def update_task(db: SessionDEP, user: UserDEP, id: int, data: TaskCreate):
    return TaskService.update_task(db, user, id, data)

@router.delete(
    '/{id:int}/',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='刪除現有任務'
    )
def delete_task(db: SessionDEP, user: UserDEP, id: int):
    return TaskService.delete_task(db, user, id)

