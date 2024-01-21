from typing import Optional

from fastapi import Depends

from app.repositories.tasks import TasksRepository, get_tasks_repository

from app.schemas.task import Task, TaskCreate


class TaskService:
    def __init__(
        self, task_repo: TasksRepository = Depends(get_tasks_repository)
    ) -> None:
        self.task_repo = task_repo
    
    def get_all_by_owner(self, owner_id: str, skip: int, limit: int) -> list[Task]:
        return self.task_repo.get_all_by_owner(owner_id=owner_id, skip=skip, limit=limit)
    
    def get_by_id(self, id: str) -> Optional[Task]:
        return self.task_repo.get(obj_id=id)
    
    def create_with_owner(self, obj_create: TaskCreate, owner_id: str) -> Task:
        order = self.task_repo.get_max_order(owner_id=owner_id)
        obj_create.order = order + 1
        return self.task_repo.create_with_owner(obj_create=obj_create, owner_id=owner_id)
    
    def update_order(self, id: str, order: int) -> Optional[Task]:
        return self.task_repo.update_order(id=id, order=order)
    
    def delete(self, id: str) -> Optional[Task]:
        deleted = self.task_repo.delete(obj_id=id)
        return deleted
    
    def update_status(self, id: str, status: bool) -> Optional[Task]:
        return self.task_repo.update_status(id=id, status=status)
    
    def update_title(self, id: str, title: str) -> Optional[Task]:
        return self.task_repo.update_title(id=id, title=title)
    
    def delete_with_order_update(self, id: str) -> Optional[Task]:
        return self.task_repo.delete_with_order_update(id=id)