from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, \
    Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from enum import IntEnum

from .database import Base


class Difficulty(IntEnum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
    

class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable=True)
    
    user = relationship('User', back_populates='tasks')
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    difficulty = Column(Enum(Difficulty), default=Difficulty.MEDIUM, nullable=False)
    tag = relationship('Tag', back_populates='tasks')
    priority = Column(Enum(Priority), default=Priority.MEDIUM, nullable=False)
    deadline = Column(DateTime, nullable=True)
    
    create_at = Column(DateTime, default=func.now(), nullable=False)
    

class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    
    name = Column(String, unique=True, nullable=False)
    is_public = Column(Boolean, default=True, nullable=False)
    owner = relationship('User', back_populates='tags')
    
    tasks = relationship('Task', back_populates='tag')