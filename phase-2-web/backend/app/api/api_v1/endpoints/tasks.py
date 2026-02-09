from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.models.task import Task, TaskCreate, TaskUpdate, TaskRead
from app.models.user import User
from app.auth.middleware import get_current_user_id, verify_user_owns_resource
from uuid import UUID
from typing import List


router = APIRouter()


@router.get("/{user_id}/tasks", response_model=List[TaskRead])
async def get_tasks(user_id: str, current_user_id: str = Depends(get_current_user_id), session: AsyncSession = Depends(get_async_session)):
    try:
        # Verify that the token user_id matches the URL user_id
        verify_user_owns_resource(current_user_id, user_id)

        # Get all tasks for the specified user
        statement = select(Task).where(Task.user_id == UUID(user_id))
        result = await session.execute(statement)
        tasks = result.scalars().all()

        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tasks: {str(e)}"
        )


@router.post("/{user_id}/tasks", response_model=TaskRead)
async def create_task(user_id: str, task: TaskCreate, current_user_id: str = Depends(get_current_user_id), session: AsyncSession = Depends(get_async_session)):
    try:
        # Verify that the token user_id matches the URL user_id
        verify_user_owns_resource(current_user_id, user_id)

        # Validate that title is provided
        if not task.title or task.title.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Title is required"
            )

        # Create new task
        db_task = Task(
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=UUID(user_id)
        )
        session.add(db_task)
        await session.commit()
        await session.refresh(db_task)
        return db_task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}"
        )


@router.get("/{user_id}/tasks/{id}", response_model=TaskRead)
async def get_task(user_id: str, id: str, current_user_id: str = Depends(get_current_user_id), session: AsyncSession = Depends(get_async_session)):
    try:
        # Verify that the token user_id matches the URL user_id
        verify_user_owns_resource(current_user_id, user_id)

        # Get specific task for the specified user
        statement = select(Task).where(and_(Task.id == UUID(id), Task.user_id == UUID(user_id)))
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving task: {str(e)}"
        )


@router.put("/{user_id}/tasks/{id}", response_model=TaskRead)
async def update_task(user_id: str, id: str, task_update: TaskUpdate, current_user_id: str = Depends(get_current_user_id), session: AsyncSession = Depends(get_async_session)):
    try:
        # Verify that the token user_id matches the URL user_id
        verify_user_owns_resource(current_user_id, user_id)

        # Validate that title is provided if it's being updated
        if task_update.title is not None and (not task_update.title or task_update.title.strip() == ""):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Title is required"
            )

        # Find and update the task
        statement = select(Task).where(and_(Task.id == UUID(id), Task.user_id == UUID(user_id)))
        result = await session.execute(statement)
        db_task = result.scalar_one_or_none()

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Update task fields if provided
        if task_update.title is not None:
            db_task.title = task_update.title
        if task_update.description is not None:
            db_task.description = task_update.description
        if task_update.completed is not None:
            db_task.completed = task_update.completed

        session.add(db_task)
        await session.commit()
        await session.refresh(db_task)
        return db_task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating task: {str(e)}"
        )


@router.delete("/{user_id}/tasks/{id}")
async def delete_task(user_id: str, id: str, current_user_id: str = Depends(get_current_user_id), session: AsyncSession = Depends(get_async_session)):
    try:
        # Verify that the token user_id matches the URL user_id
        verify_user_owns_resource(current_user_id, user_id)

        # Find and delete the task
        statement = select(Task).where(and_(Task.id == UUID(id), Task.user_id == UUID(user_id)))
        result = await session.execute(statement)
        db_task = result.scalar_one_or_none()

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        await session.delete(db_task)
        await session.commit()
        return {"message": "Task deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting task: {str(e)}"
        )


@router.patch("/{user_id}/tasks/{id}/complete", response_model=TaskRead)
async def update_task_completion(user_id: str, id: str, task_data: dict, current_user_id: str = Depends(get_current_user_id), session: AsyncSession = Depends(get_async_session)):
    try:
        # Verify that the token user_id matches the URL user_id
        verify_user_owns_resource(current_user_id, user_id)

        # Extract completed status from request
        completed = task_data.get("completed")
        if completed is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Completed status is required"
            )

        # Find and update the task completion status
        statement = select(Task).where(and_(Task.id == UUID(id), Task.user_id == UUID(user_id)))
        result = await session.execute(statement)
        db_task = result.scalar_one_or_none()

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Update completion status
        db_task.completed = completed

        session.add(db_task)
        await session.commit()
        await session.refresh(db_task)
        return db_task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating task completion: {str(e)}"
        )