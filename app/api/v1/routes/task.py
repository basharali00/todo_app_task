from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException

from app.core.deps import get_current_user
from app.schemas.user import User
from app.schemas.task import TaskCreate, Task
from app.services.task import TaskService

router = APIRouter()

@router.get("/", response_model=List[Task])
def get_tasks( 
            task_service: TaskService = Depends(),
            user: User = Depends(get_current_user),
            skip: int = 0,
            limit: int = 100
        ) -> Task:

    tasks = task_service.get_all_by_owner(owner_id=user.id, skip=skip, limit=limit)

    return tasks

@router.post("", response_model=Task)
def create_task(
    task_create: TaskCreate,
    task_service: TaskService = Depends(),
    user: User = Depends(get_current_user)
) -> Task:
    return task_service.create_with_owner(obj_create=task_create, owner_id=user.id)


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: str, 
             task_service: TaskService = Depends(),
             user: User = Depends(get_current_user)) -> Task:
    task = task_service.get_by_id(id=task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.owner_id != user.id:
        raise HTTPException(status_code=403, detail="No Permissions")
    
    return task

@router.put("/{task_id}/order", response_model=Task)
def update_task_order(
    task_id: str,
    order: int,
    task_service: TaskService = Depends(),
    user: User = Depends(get_current_user)
) -> Task:
    task = task_service.update_order(id=task_id, order=order)

    if task.owner_id != user.id:
        raise HTTPException(status_code=403, detail="No Permissions")
    
    return task

@router.put("/{task_id}/status", response_model=Task)
def update_task_status(
    task_id: str,
    status: bool,
    task_service: TaskService = Depends(),
    user: User = Depends(get_current_user)
) -> Task:
    task = task_service.update_status(id=task_id, status=status)

    if task.owner_id != user.id:
        raise HTTPException(status_code=403, detail="No Permissions")
    
    return task

@router.put("/{task_id}/title", response_model=Task)
def update_task_title(
    task_id: str,
    title: str,
    task_service: TaskService = Depends(),
    user: User = Depends(get_current_user)
) -> Task:
    task = task_service.update_title(id=task_id, title=title)

    if task.owner_id != user.id:
        raise HTTPException(status_code=403, detail="No Permissions")
    
    return task

@router.delete("/{task_id}", response_model=Task)
def delete_task(
    task_id: str,
    task_service: TaskService = Depends(),
    user: User = Depends(get_current_user)
) -> Task:
    task = task_service.delete_with_order_update(id=task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.owner_id != user.id:
        raise HTTPException(status_code=403, detail="No Permissions")
    
    return task