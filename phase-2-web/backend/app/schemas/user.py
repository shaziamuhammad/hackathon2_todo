from pydantic import BaseModel
from typing import List
from .task import Task


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    tasks: List[Task] = []

    class Config:
        from_attributes = True