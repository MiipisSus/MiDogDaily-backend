from fastapi import  Depends
from sqlalchemy.orm import Session
from typing import Annotated

from app.core.models import get_db, User
from app.services.auth import AuthService

# DB Session
SessionDEP = Annotated[Session, Depends(get_db)]

# Authorization
UserDEP = Annotated[User, Depends(AuthService.is_user)]
SuperUserDEP = Annotated[User, Depends(AuthService.is_superuser)]
AdminDEP = Annotated[User, Depends(AuthService.is_admin)]