from pytest import fixture
from sqlalchemy.orm import Session
from typing import Callable, Generator

from app.core.models import User, Role


@fixture(scope='function')
def create_user(db: Session):
    users = []
    
    def _create_user(username: str = 'user', role_id: int = Role.USER):
        nonlocal users
        user = User(**create_user_data(username, role_id))
        user.encode_password()

        db.add(user)
        db.commit()
        db.refresh(user)
        
        users.append(user)
        return user
    
    yield _create_user

    for user in users:
        db.delete(user)
    db.commit()
    
def create_user_data(username: str, role_id: int):
    return {
        'username': username,
        'email': f"{username}@example.com",
        'password': "12345",
        'role_id': role_id
    }