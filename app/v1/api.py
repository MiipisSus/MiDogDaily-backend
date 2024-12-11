from fastapi import APIRouter
from .endpoints import *


router = APIRouter()

router.include_router(user_router, prefix='/users', tags=['Users'])