# phase-2-web\backend\app\models\user.py
from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
from pydantic import BaseModel

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True, nullable=False)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: Optional[str] = Field(default=None)  # Optional for OAuth users
    name: Optional[str] = Field(default=None)
    theme_preference: str = Field(default="light")  # light, dark, purple
    provider: str = Field(default="email")  # email, google, facebook
    provider_id: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="owner")


class UserCreate(UserBase):
    email: str
    password: str
    name: Optional[str] = None


class UserRead(UserBase):
    id: uuid.UUID
    name: Optional[str] = None
    theme_preference: str
    provider: str
    created_at: datetime
    updated_at: datetime

class LoginRequest(BaseModel):
    email: str
    password: str