from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
from passlib.context import CryptContext

from .database import Base


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    
    nickname = Column(String)
    coin = Column(Float)
    tasks = relationship('Task', back_populates='user')
    tags = relationship('Tag', back_populates='owner')
    
    def encode_password(self):        
        self.password = pwd_context.hash(self.password)