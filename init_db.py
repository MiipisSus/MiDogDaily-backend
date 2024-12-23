from sqlalchemy.orm import Session
from app.core.models import User, Tag, UserRole
from app.core.models.database import SessionLocal

def init_db():
    db = SessionLocal()
    try:
        # 添加初始使用者角色
        init_roles(db)
        
        # 添加管理員
        init_admin(db)

        # 添加初始標籤
        init_tags(db)
    finally:
        db.close()
        
def init_roles(db: Session):
    roles = ['管理員', '超級使用者', '一般使用者']
    for role_name in roles:
        if not db.query(UserRole).filter(UserRole.name == role_name).first():
            role = UserRole(
                name=role_name,
            )
            db.add(role)
    
    db.commit()        
    
def init_admin(db: Session):
    admin = db.query(User).filter(User.username == 'admin').first()
    if not admin:
        admin = User(
            username="admin",
            email="admin@example.com",
            password="12345",  # 替換為加密密碼
            role_id=1,
        )
        admin.encode_password()
        
        db.add(admin)
        db.commit()
        db.refresh(admin)

def init_tags(db: Session):
    admin = db.query(User).filter(User.username == 'admin').first()
    
    tags = ["工作", "學習", "活動"]
    for tag_name in tags:
        if not db.query(Tag).filter(Tag.name == tag_name).first():
            tag = Tag(
                name=tag_name,
                is_public=True,
                owner_id=admin.id
                )
            db.add(tag)

    db.commit()
    
if __name__ == "__main__":
    init_db()