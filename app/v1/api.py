from fastapi import APIRouter
from .endpoints import *


router = APIRouter()

router.include_router(user_router, prefix='/users', tags=['Users'])
router.include_router(task_router, prefix='/tasks', tags=['Tasks'])
router.include_router(tag_router, prefix='/tags', tags=['Tags'])
router.include_router(auth_router, prefix='/auth', tags=['Auth'])