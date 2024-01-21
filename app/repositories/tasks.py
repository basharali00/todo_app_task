from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import get_app_settings
from .base import BaseRepository
from app.db.session import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

settings = get_app_settings()

class TasksRepository(BaseRepository[Task, TaskCreate, TaskUpdate]):
    def get_all_by_owner(
        self, owner_id: str, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        return (
            self.db.query(self.model)
            .filter(Task.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    def create_with_owner(self, obj_create: TaskCreate, owner_id: str) -> Task:
        obj = self.model(**obj_create.model_dump(), owner_id=owner_id)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def get_max_order(self, owner_id: str) -> int:
        return (
            self.db.query(self.model)
            .filter(Task.owner_id == owner_id)
            .count()
        )

    def update_title(self, id: str, title: str) -> Task:
        task = self.get(obj_id=id)
        task.title = title
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def update_order(self, id: str, order: int) -> Task:
        task = self.get(obj_id=id)
        old_order = task.order

        task.order = order
        self.db.commit()
        self.db.refresh(task)

        #  update order of tasks between old and new order
        if old_order < order:
            self.db.query(self.model).filter(
                Task.owner_id == task.owner_id,
                Task.id != task.id,
                Task.order <= order,
                Task.order > old_order
            ).update({Task.order: Task.order - 1})
        else:
            self.db.query(self.model).filter(
                Task.owner_id == task.owner_id,
                Task.order >= order,
                Task.order < old_order
            ).update({Task.order: Task.order + 1})
        
        return task
    
    def update_status(self, id: str, status: bool) -> Task:
        task = self.get(obj_id=id)
        task.status = status
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_with_order_update(self, id: str) -> Task:
        task = self.get(obj_id=id)

        if task:
            order = task.order

            self.db.delete(task)
            self.db.commit()
            
            self.db.query(self.model).filter(
                Task.owner_id == task.owner_id,
                Task.order > order
            ).update({Task.order: Task.order - 1})
            self.db.commit()
            
            return task
    
def get_tasks_repository(session: Session = Depends(get_db)) -> TasksRepository:
    return TasksRepository(db=session, model=Task)
