from pytest import fixture
from sqlalchemy.orm import Session
from typing import Callable, Generator
from datetime import datetime, timedelta
import random

from faker import Faker

from app.core.models import User, Role, Task, Tag

faker = Faker()

@fixture(scope='function')
def create_user(db: Session):
    def _create_user(role_id: int = Role.USER):
        user = User(**create_user_data(role_id))
        user.encode_password()

        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    
    return _create_user
    
def create_user_data(role_id: int = Role.USER):
    username = faker.first_name()
    
    return {
        'username': username,
        'email': f"{username}@example.com",
        'password': "12345",
        'role_id': role_id
    }
    
@fixture(scope='function')
def create_task(db: Session):
    def _create_task(user_id: int, tag_ids: list = []):
        task = Task(**create_task_data(user_id, tag_ids), user_id=user_id)
        
        db.add(task)
        db.commit()
        db.refresh(task)

        return task
    
    return _create_task

def create_task_data(tag_ids: list = [], json_format=False):
    future_date = datetime.now() + timedelta(days=random.randint(1, 30))
    if json_format:
        future_date = future_date.isoformat()
        
    return {
        'title': faker.text(max_nb_chars=5),
        'content': faker.text(max_nb_chars=5),
        'difficulty': 'MEDIUM',
        'priority': 'MEDIUM',
        'deadline': future_date,
        'tag_ids': tag_ids
    }
    
@fixture(scope='function')
def create_tag(db: Session):
    def _create_tag(owner_id: int, is_public: bool = False):
        tag = Tag(**create_tag_data(),
                  owner_id=owner_id,
                  is_public=is_public)
        
        db.add(tag)
        db.commit()
        db.refresh(tag)
        
        return tag
    
    return _create_tag

def create_tag_data():
    name = faker.text(max_nb_chars=5)
    
    return {
        'name': name
    }
