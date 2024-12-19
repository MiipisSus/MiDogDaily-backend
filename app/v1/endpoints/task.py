from fastapi import APIRouter, status, Query
from fastapi_pagination import Page

from app.core.schemas import TaskCreate, TaskResponse
from app.services import TaskService
from app.deps import SessionDEP, UserDEP

router = APIRouter()


@router.get(
    '/',
    response_model=Page[TaskResponse],
    summary='獲取該位使用者的所有任務'
    )
def list_tasks(
    db: SessionDEP,
    user: UserDEP,
    user_id: int = Query(description='使用者的 ID')
    ):
    return TaskService.list_tasks(db, user, user_id)

@router.post('/', response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(db: SessionDEP, user: UserDEP, data: TaskCreate):
    return TaskService.create_task(db, user, data)

@router.put('/{id}', response_model=TaskResponse)
def update_task(db: SessionDEP, user: UserDEP, id: int, data: TaskCreate):
    return TaskService.update_task(db, user, id, data)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(db: SessionDEP, user: UserDEP, id: int):
    return TaskService.delete_task(db, user, id)

