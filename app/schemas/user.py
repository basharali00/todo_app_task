from pydantic import BaseModel, EmailStr
from .task import Task

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    tasks: list[Task] = []

    class Config:
        orm_mode = True

class UserInDB(User):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    pass