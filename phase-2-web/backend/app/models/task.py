from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid


class TaskBase(SQLModel):
    title: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    priority: Optional[str] = Field(default="medium")  # low, medium, high, urgent
    status: Optional[str] = Field(default="pending")  # pending, in-progress, complete


class Task(TaskBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    priority: str = Field(default="medium")
    status: str = Field(default="pending")
    tags: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    due_date: Optional[datetime] = Field(default=None)
    recurrence_pattern: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    completed_at: Optional[datetime] = Field(default=None)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    owner: Optional["User"] = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    tags: Optional[List[str]] = None
    due_date: Optional[datetime] = None
    recurrence_pattern: Optional[Dict[str, Any]] = None


class TaskUpdate(TaskBase):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    tags: Optional[List[str]] = None
    due_date: Optional[datetime] = None
    recurrence_pattern: Optional[Dict[str, Any]] = None


class TaskRead(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    priority: str
    status: str
    tags: Optional[List[str]] = None
    due_date: Optional[datetime] = None
    recurrence_pattern: Optional[Dict[str, Any]] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime