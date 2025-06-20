from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from datetime import datetime, timedelta

from app.core.models import Task, User, TaskTagLink
from app.core.filters import TaskRangeParams
from app.core.schemas import TaskCreate
from .tag import TagService
from .utils import update_instance, validate_user_access


class TaskService:
    """處理任務相關的業務邏輯"""
    
    class Exceptions:
        @staticmethod
        def task_not_found(id: int) -> HTTPException:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Task with id {id} does not exist'
            )
        
    @classmethod
    def _get_task_by_id(cls, db: Session, id: int):
        task = db.query(Task).filter(Task.id == id).first()
        if not task:
            raise cls.Exceptions.task_not_found(id)
        
        return task
    
    @classmethod
    def list_tasks(cls, db: Session, user: User, query) -> Page[Task]:
        today = datetime.today().date()
        tasks = db.query(Task).filter(Task.user_id == user.id)
        
        if query.get("date"):
            date = query.get("date")
            start_of_day = datetime.combine(date, datetime.min.time())
            end_of_day = datetime.combine(date, datetime.max.time())
            tasks = tasks.filter(Task.deadline.between(start_of_day, end_of_day))
        elif query.get('range'):
            range = query.get('range')
            if range == TaskRangeParams.today:
                start_of_day = datetime.combine(today, datetime.min.time())
                end_of_day = datetime.combine(today, datetime.max.time())

                tasks = tasks.filter(Task.deadline.between(start_of_day, end_of_day))
            elif range == TaskRangeParams.week:
                start_of_week = today - timedelta(days=today.weekday())
                end_of_week = start_of_week + timedelta(days=6)
                tasks = tasks.filter(Task.deadline.between(start_of_week, end_of_week))
            elif range == TaskRangeParams.month:
                start_of_month = today.replace(day=1)
                next_month = start_of_month.replace(month=start_of_month.month % 12 + 1, day=1)
                end_of_month = next_month - timedelta(days=1)
                tasks = tasks.filter(Task.deadline.between(start_of_month, end_of_month))

        tasks = tasks.filter(Task.is_completed == query.get('is_completed'))
        # order
        tasks = tasks.order_by(Task.deadline)
        
        return paginate(tasks)
    
    @classmethod
    def get_task(cls, db: Session, user: User, id: int):
        task = cls._get_task_by_id(db, id)
        validate_user_access(user, task.user_id)

        return task
    
    @classmethod
    def create_task(cls, db: Session, user: User, data: TaskCreate):
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
            tag = TagService._get_tag_by_id(db, tag_id)
            # 檢查該 tag 是否屬於該用戶，或者為公開
            if not (tag.is_public or tag.owner_id == user.id):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
            
            task_tag = TaskTagLink(task_id=new_task.id, tag_id=tag_id)
            db.add(task_tag)
        
        db.commit()
        
        return new_task
    
    @classmethod
    def update_task(cls, db: Session, user: User, id: int, data: TaskCreate):
        task = cls._get_task_by_id(db, id)
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
            tag = TagService._get_tag_by_id(db, tag_id)
            # 檢查該 tag 是否屬於該用戶，或者為公開
            if not (tag.is_public or tag.owner_id == user.id):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
            
            task_tag = TaskTagLink(task_id=task.id, tag_id=tag_id)
            db.add(task_tag)
        
        update_instance(task, data)
            
        db.commit()
        db.refresh(task)
            
        return task
    
    @classmethod
    def delete_task(cls, db: Session, user: User, id: int):
        task = cls._get_task_by_id(db, id)
        validate_user_access(user, task.user_id)
        
        db.delete(task)
        db.commit()
        
        return task