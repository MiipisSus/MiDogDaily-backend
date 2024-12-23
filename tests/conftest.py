from pytest import fixture
from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from app.core.models import get_db
from fastapi.testclient import TestClient

from app.main import app
from init_db import init_admin, init_roles, init_tags


# 測試資料庫設置
TEST_DATABASE_URL = 'sqlite:///./test.db'
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@fixture(scope='session')
def db():
    """提供整個測試 session 使用的資料庫連接"""
    # 創建所有表
    SQLModel.metadata.create_all(bind=engine)
    
    # 創建會話
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        SQLModel.metadata.drop_all(bind=engine)

@fixture(scope='function')
def client(db: Session):
    """提供測試用的 API 客戶端"""
    app.dependency_overrides[get_db] = lambda: db
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()

@fixture(scope='function', autouse=True)
def setup_and_cleanup(db: Session):
    """每個測試前的設置和清理"""
    # 清理所有表
    SQLModel.metadata.drop_all(bind=engine)
    SQLModel.metadata.create_all(bind=engine)
    
    # 初始化基礎數據
    init_roles(db)
    init_admin(db)
    init_tags(db)
    db.commit()
    
    yield
    
    # 測試後清理
    db.close()
