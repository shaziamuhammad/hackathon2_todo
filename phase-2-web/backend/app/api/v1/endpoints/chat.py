"""
Chat endpoint for AI-powered todo management
Uses OpenAI Assistants API with MCP tool integration
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.auth.middleware import get_current_user_id
from app.ai_agent.agent import get_assistant
from slowapi import Limiter
from slowapi.util import get_remote_address
import sys
import os
import logging

# Import MCP tools
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from app.mcp_server import add_task, list_tasks, update_task, delete_task, mark_complete

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None  # Thread ID for conversation continuity


class ChatResponse(BaseModel):
    response: str
    conversation_id: str


# Store for conversation threads (in production, use Redis or database)
conversation_threads: Dict[str, str] = {}


@router.post("/chat", response_model=ChatResponse, summary="Process natural language todo commands")
@limiter.limit("20/minute")  # Rate limit: 20 requests per minute per IP
async def chat(
    http_request: Request,
    request: ChatRequest,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Chat with the AI assistant for todo task management.

    Args:
        request: Chat request containing message and optional conversation_id
        current_user_id: Current authenticated user ID

    Returns:
        ChatResponse with assistant's response and conversation_id
    """
    try:
        # Validate request
        if not request.message or not request.message.strip():
            logger.warning(f"Empty message received from user {current_user_id}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Message cannot be empty"
            )

        # Validate message length
        if len(request.message) > 2000:
            logger.warning(f"Message too long from user {current_user_id}: {len(request.message)} chars")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Message must be 2000 characters or less"
            )

        logger.info(f"Processing chat message for user {current_user_id}")

        # Prepare MCP tool handlers
        tool_handlers = {
            "add_task": add_task,
            "list_tasks": list_tasks,
            "update_task": update_task,
            "delete_task": delete_task,
            "mark_complete": mark_complete
        }

        # Get or create assistant
        assistant = await get_assistant(tool_handlers)

        # Get or create conversation thread
        thread_id = request.conversation_id
        if not thread_id or thread_id not in conversation_threads:
            thread_id = await assistant.create_thread()
            conversation_threads[thread_id] = current_user_id
            logger.info(f"Created new conversation thread {thread_id} for user {current_user_id}")

        # Verify thread belongs to current user
        if conversation_threads.get(thread_id) != current_user_id:
            logger.warning(f"User {current_user_id} attempted to access thread {thread_id} owned by another user")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this conversation"
            )

        # Add user message to thread
        await assistant.add_message(thread_id, request.message)
        logger.debug(f"Added message to thread {thread_id}")

        # Run assistant and get response
        response_text = await assistant.run_assistant(thread_id, current_user_id)
        logger.info(f"AI assistant generated response for user {current_user_id}")

        return ChatResponse(
            response=response_text,
            conversation_id=thread_id
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat error for user {current_user_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat error: {str(e)}"
        )


@router.delete("/chat/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Delete a conversation thread.

    Args:
        conversation_id: The thread ID to delete
        current_user_id: Current authenticated user ID

    Returns:
        Success message
    """
    try:
        # Verify thread belongs to current user
        if conversation_threads.get(conversation_id) != current_user_id:
            logger.warning(f"User {current_user_id} attempted to delete thread {conversation_id} owned by another user")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this conversation"
            )

        # Remove from storage
        if conversation_id in conversation_threads:
            del conversation_threads[conversation_id]
            logger.info(f"Deleted conversation {conversation_id} for user {current_user_id}")

        return {"message": "Conversation deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting conversation {conversation_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting conversation: {str(e)}"
        )
