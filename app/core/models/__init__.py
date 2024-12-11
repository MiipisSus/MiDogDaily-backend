from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends

from .database import Base, engine, SessionLocal
from .task import *
from .user import *


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]