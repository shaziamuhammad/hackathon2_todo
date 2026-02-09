"""
Chat API endpoint schemas
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class ChatRequest(BaseModel):
    """Request schema for chat endpoint"""
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Response schema for chat endpoint"""
    response: str
    action_taken: str
    tasks_modified: List[Dict[str, Any]] = []
    conversation_id: Optional[str] = None
