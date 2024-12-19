from sqlmodel import SQLModel
from fastapi import HTTPException, status

from app.core.models import User, Role


def update_instance(obj, data: SQLModel):
    """
    實例更新
    """
    for field, value in data.model_dump().items():
        if hasattr(obj, field):
            setattr(obj, field, value)
    
    # User 密碼重新加密
    if isinstance(obj, User):
        obj.encode_password()
            
def validate_user_access(user: User, user_id):
    """
    檢查該用戶是否為該實例擁有者，或者是否有管理員權限
    """
    if user.id != user_id and user.role_id != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)