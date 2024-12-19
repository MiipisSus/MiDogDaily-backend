from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from app.core.models import Task, User, TaskTagLink
from app.core.schemas import TaskCreate
from .tag import TagService
from .utils import update_instance, validate_user_access


class TaskService:
    @staticmethod
    def is_task_exist(db: Session, id: int):
        task = db.query(Task).filter(Task.id == id).first()
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task with id {id} does not exist')
        
        return task
    
    @staticmethod
    def list_tasks(db: Session, user: User, user_id: int) -> Page[Task]:
        validate_user_access(user, user_id)
        
        return paginate(db.query(Task).filter(Task.user_id==user_id))
    
    @staticmethod
    def create_task(db: Session, user: User, data: TaskCreate):
        data = data.model_dump()
        tag_ids = data.pop('tag_ids')
        
        new_task = Task(
            **data,
            user_id=user.id
        )
        
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        
        for tag_id in tag_ids:
            # 檢查該 tag 是否存在
            tag = TagService.is_tag_exist(db, tag_id)
            # 檢查該 tag 是否屬於該用戶，或者為公開
            if not (tag.is_public or tag.owner_id == user.id):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
            
            task_tag = TaskTagLink(task_id=new_task.id, tag_id=tag_id)
            db.add(task_tag)
        
        db.commit()
        
        return new_task
    
    @staticmethod
    def update_task(db: Session, user: User, id: int, data: TaskCreate):
        task = TaskService.is_task_exist(db, id)
        validate_user_access(user, task.user_id)
        
        tag_ids = set(data.model_dump().pop('tag_ids'))
        
        current_tag_ids = {tag.id for tag in task.tags}
        
        tags_to_add = tag_ids - current_tag_ids
        tags_to_remove = current_tag_ids - tag_ids
        
        if tags_to_remove:
            db.query(TaskTagLink).filter(
                TaskTagLink.task_id == task.id,
                TaskTagLink.tag_id.in_(tags_to_remove)
            ).delete(synchronize_session=False)
        
        for tag_id in tags_to_add:
            # 檢查該 tag 是否存在
            tag = TagService.is_tag_exist(db, tag_id)
            # 檢查該 tag 是否屬於該用戶，或者為公開
            if not (tag.is_public or tag.owner_id == user.id):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
            
            task_tag = TaskTagLink(task_id=task.id, tag_id=tag_id)
            db.add(task_tag)
        
        update_instance(task, data)
        
        db.commit()
        db.refresh(task)
        
        return task
    
    @staticmethod
    def delete_task(db: Session, user: User, id: int):
        task = TaskService.is_task_exist(db, id)
        validate_user_access(user, task.user_id)
        
        db.delete(task)
        db.commit()
        
        return task