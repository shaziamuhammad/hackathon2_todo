from sqlmodel import SQLModel, Field, Column, JSON
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid


class ConversationBase(SQLModel):
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)


class Conversation(ConversationBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, index=True)
    thread_id: str = Field(nullable=False, unique=True, index=True)  # OpenAI thread ID
    title: Optional[str] = Field(default=None, max_length=200)  # Auto-generated from first message
    messages: List[Dict[str, Any]] = Field(default_factory=list, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_message_at: Optional[datetime] = Field(default=None)
    message_count: int = Field(default=0)


class ConversationCreate(ConversationBase):
    user_id: uuid.UUID
    thread_id: str
    title: Optional[str] = None


class ConversationRead(ConversationBase):
    id: uuid.UUID
    thread_id: str
    title: Optional[str]
    message_count: int
    created_at: datetime
    updated_at: datetime
    last_message_at: Optional[datetime]


class ConversationDetail(ConversationRead):
    """Schema for reading conversation with full message history"""
    messages: List[Dict[str, Any]]


class ConversationUpdate(SQLModel):
    messages: Optional[List[Dict[str, Any]]] = None
    title: Optional[str] = None
    last_message_at: Optional[datetime] = None
    message_count: Optional[int] = None

