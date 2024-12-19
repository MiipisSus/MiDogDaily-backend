from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends

from .database import SessionLocal
from .task import *
from .user import *
from .tag import *

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()