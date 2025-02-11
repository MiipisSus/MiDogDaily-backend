from fastapi import APIRouter, status, Query
from fastapi_pagination import Page

from app.core.schemas import TagCreate, TagResponse
from app.services import TagService
from app.deps import SessionDEP, UserDEP


router = APIRouter()


@router.get(
    '/',
    response_model=Page[TagResponse],
    summary='獲取該位使用者的所有自訂標籤，以及公共標籤'
    )
def list_tags(
    db: SessionDEP,
    user: UserDEP,
    is_public: bool = Query(description='是否獲取公共標籤')
    ):
    return TagService.list_tags(db, user, is_public)

@router.post(
    '/',
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED,
    summary='創建新標籤',
    description='如果是由管理員創建的話，則是公共標籤，反之則為私人標籤'
)
def create_tag(db: SessionDEP, user: UserDEP, data: TagCreate):
    return TagService.create_tag(db, user, data)

@router.put(
    '/{id}/',
    response_model=TagResponse,
    summary='更新單一標籤'
)
def update_tag(db: SessionDEP, user: UserDEP, id: int, data: TagCreate):
    return TagService.update_tag(db, user, id, data)

@router.delete(
    '/{id}/',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='刪除單一標籤'
)
def delete_tag(db: SessionDEP, user: UserDEP, id: int):
    return TagService.delete_tag(db, user, id)
