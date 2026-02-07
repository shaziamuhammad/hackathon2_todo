from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
from app.schemas.task import Task, TaskCreate, TaskUpdate, TaskComplete
from app.models.task import Task as TaskModel
from app.models.user import User
from app.api.deps import get_current_user_id, verify_user_owns_resource, get_db_session
from datetime import datetime

router = APIRouter()


@router.get("/tasks", response_model=List[Task], summary="Get all tasks for a user")
async def get_tasks(
    user_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    # Verify that the token user_id matches the URL user_id
    verify_user_owns_resource(current_user_id, user_id)

    # Get all tasks for the specified user
    tasks = db.query(TaskModel).filter(TaskModel.user_id == user_id).all()
    return tasks


@router.post("/tasks", response_model=Task, summary="Create a new task for a user")
async def create_task(
    user_id: int,
    task: TaskCreate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    # Verify that the token user_id matches the URL user_id
    verify_user_owns_resource(current_user_id, user_id)

    # Validate that title is provided
    if not task.title or task.title.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Title is required"
        )

    # Create new task
    db_task = TaskModel(
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=user_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/tasks/{id}", response_model=Task, summary="Get a specific task for a user")
async def get_task(
    user_id: int,
    id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    # Verify that the token user_id matches the URL user_id
    verify_user_owns_resource(current_user_id, user_id)

    # Get specific task for the specified user
    task = db.query(TaskModel).filter(and_(TaskModel.id == id, TaskModel.user_id == user_id)).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.put("/tasks/{id}", response_model=Task, summary="Update a specific task for a user")
async def update_task(
    user_id: int,
    id: int,
    task_update: TaskUpdate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    # Verify that the token user_id matches the URL user_id
    verify_user_owns_resource(current_user_id, user_id)

    # Validate that title is provided
    if not task_update.title or task_update.title.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Title is required"
        )

    # Find and update the task
    db_task = db.query(TaskModel).filter(and_(TaskModel.id == id, TaskModel.user_id == user_id)).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update task fields
    db_task.title = task_update.title
    db_task.description = task_update.description
    db_task.completed = task_update.completed
    db_task.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete("/tasks/{id}", summary="Delete a specific task for a user")
async def delete_task(
    user_id: int,
    id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    # Verify that the token user_id matches the URL user_id
    verify_user_owns_resource(current_user_id, user_id)

    # Find and delete the task
    db_task = db.query(TaskModel).filter(and_(TaskModel.id == id, TaskModel.user_id == user_id)).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}


@router.patch("/tasks/{id}/complete", response_model=Task, summary="Mark a task as complete/incomplete")
async def update_task_completion(
    user_id: int,
    id: int,
    task_complete: TaskComplete,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
):
    # Verify that the token user_id matches the URL user_id
    verify_user_owns_resource(current_user_id, user_id)

    # Find and update the task completion status
    db_task = db.query(TaskModel).filter(and_(TaskModel.id == id, TaskModel.user_id == user_id)).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update completion status
    db_task.completed = task_complete.completed
    db_task.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_task)
    return db_task