from fastapi import APIRouter, status, Query
from fastapi_pagination import Page
from typing import Optional
from enum import Enum
from datetime import date

from app.core.schemas import TaskCreate, TaskResponse
from app.core.filters import TaskRangeParams
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
    range: Optional[TaskRangeParams] = Query(default=None, description='快速選擇日期範圍'),
    date: Optional[date] = Query(default=None, description='指定日期（若 range 有值，則略過）'),
    is_completed: Optional[bool] = Query(default=False, description='是否獲取已完成任務'),
    ):
    query = {
        'range': range,
        'date': date,
        'is_completed': is_completed
    }
    return TaskService.list_tasks(db, user, query)

@router.get(
    '/{id:int}/',
    response_model=TaskResponse,
    summary='獲取單一任務'
)
def get_task(
    db: SessionDEP,
    user: UserDEP,
    id: int,
    ):
    return TaskService.get_task(db, user, id)

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