from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    status: bool = False
    order: int

class TaskCreate(TaskBase):
    pass

class TaskUpdateStatus(BaseModel):
    id: str
    status: bool

class TaskUpdateOrder(BaseModel):
    id: str
    order: int

class TaskUpdate(BaseModel):
    id: str
    title: str

class Task(TaskBase):
    id: str
    owner_id: str

    class Config:
        orm_mode = True