"""
Conversation management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from datetime import datetime

from app.models.conversation import (
    Conversation,
    ConversationRead,
    ConversationDetail,
    ConversationCreate
)
from app.auth.middleware import get_current_user_id
from app.db.session import get_async_session

router = APIRouter()


@router.get("/conversations", response_model=List[ConversationRead])
async def list_conversations(
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    List all conversations for the current user.
    Returns conversation metadata without full message history.
    """
    try:
        statement = select(Conversation).where(
            Conversation.user_id == UUID(current_user_id)
        ).order_by(Conversation.updated_at.desc())

        result = await session.execute(statement)
        conversations = result.scalars().all()

        return conversations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing conversations: {str(e)}"
        )


@router.get("/conversations/{conversation_id}", response_model=ConversationDetail)
async def get_conversation(
    conversation_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get a specific conversation with full message history.
    """
    try:
        statement = select(Conversation).where(
            Conversation.id == UUID(conversation_id),
            Conversation.user_id == UUID(current_user_id)
        )

        result = await session.execute(statement)
        conversation = result.scalar_one_or_none()

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

        return conversation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving conversation: {str(e)}"
        )


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Delete a conversation.
    """
    try:
        statement = select(Conversation).where(
            Conversation.id == UUID(conversation_id),
            Conversation.user_id == UUID(current_user_id)
        )

        result = await session.execute(statement)
        conversation = result.scalar_one_or_none()

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

        await session.delete(conversation)
        await session.commit()

        return {"message": "Conversation deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting conversation: {str(e)}"
        )


@router.post("/conversations", response_model=ConversationRead)
async def create_conversation(
    conversation: ConversationCreate,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new conversation (usually called internally by chat endpoint).
    """
    try:
        # Verify user_id matches current user
        if str(conversation.user_id) != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot create conversation for another user"
            )

        db_conversation = Conversation(
            user_id=conversation.user_id,
            thread_id=conversation.thread_id,
            title=conversation.title,
            message_count=0
        )

        session.add(db_conversation)
        await session.commit()
        await session.refresh(db_conversation)

        return db_conversation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating conversation: {str(e)}"
        )
