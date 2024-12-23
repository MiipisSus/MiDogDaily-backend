from fastapi import APIRouter
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
def list_tags(db: SessionDEP, user: UserDEP):
    return TagService.list_tags(db, user)

@router.post('/', response_model=TagResponse)
def create_tag(db: SessionDEP, user: UserDEP, data: TagCreate):
    return TagService.create_tag(db, user, data)

@router.put('/{id}/', response_model=TagResponse)
def update_tag(db: SessionDEP, user: UserDEP, id: int, data: TagCreate):
    return TagService.update_tag(db, user, id, data)

@router.delete('/{id}/')
def delete_tag(db: SessionDEP, user: UserDEP, id: int):
    return TagService.delete_tag(db, user, id)