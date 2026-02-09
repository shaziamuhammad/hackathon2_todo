"""
MCP Server for Todo Task Management
Exposes CRUD operations as MCP tools for AI agent integration
"""
from fastmcp import FastMCP
from sqlmodel import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.models.task import Task, TaskCreate, TaskUpdate
from uuid import UUID
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

# Initialize MCP server
mcp = FastMCP("Todo Task Manager")


@mcp.tool()
async def add_task(
    user_id: str,
    title: str,
    description: Optional[str] = None,
    priority: Optional[str] = "medium",
    due_date: Optional[str] = None,
    tags: Optional[List[str]] = None,
    recurrence_pattern: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a new task for the user.

    Args:
        user_id: The UUID of the user creating the task
        title: Task title (required)
        description: Optional task description
        priority: Task priority (low, medium, high, urgent). Default: medium
        due_date: Optional due date in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
        tags: Optional list of tags
        recurrence_pattern: Optional recurrence pattern dict (e.g., {"frequency": "weekly", "interval": 1})

    Returns:
        Dict containing the created task details
    """
    try:
        # Validate title
        if not title or title.strip() == "":
            return {"error": "Title is required", "success": False}

        # Parse due_date if provided
        parsed_due_date = None
        if due_date:
            try:
                parsed_due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            except ValueError:
                return {"error": f"Invalid due_date format: {due_date}. Use ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)", "success": False}

        # Get database session
        session_gen = get_async_session()
        session = await anext(session_gen)

        try:
            # Create new task
            db_task = Task(
                title=title.strip(),
                description=description,
                priority=priority,
                user_id=UUID(user_id),
                tags=tags,
                due_date=parsed_due_date,
                recurrence_pattern=recurrence_pattern,
                completed=False,
                status="pending"
            )

            session.add(db_task)
            await session.commit()
            await session.refresh(db_task)

            return {
                "success": True,
                "task": {
                    "id": str(db_task.id),
                    "title": db_task.title,
                    "description": db_task.description,
                    "priority": db_task.priority,
                    "status": db_task.status,
                    "completed": db_task.completed,
                    "tags": db_task.tags,
                    "due_date": db_task.due_date.isoformat() if db_task.due_date else None,
                    "recurrence_pattern": db_task.recurrence_pattern,
                    "created_at": db_task.created_at.isoformat()
                }
            }
        finally:
            await session.close()
    except Exception as e:
        return {"error": f"Failed to create task: {str(e)}", "success": False}


@mcp.tool()
async def list_tasks(
    user_id: str,
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    tag: Optional[str] = None,
    sort_by: Optional[str] = "created_at",
    sort_order: Optional[str] = "desc"
) -> Dict[str, Any]:
    """
    List all tasks for a user with optional filtering and sorting.

    Args:
        user_id: The UUID of the user
        completed: Filter by completion status (True/False/None for all)
        priority: Filter by priority (low, medium, high, urgent)
        status: Filter by status (pending, in-progress, complete)
        tag: Filter by tag (tasks containing this tag)
        sort_by: Field to sort by (created_at, due_date, priority, title). Default: created_at
        sort_order: Sort order (asc, desc). Default: desc

    Returns:
        Dict containing list of tasks and count
    """
    try:
        session_gen = get_async_session()
        session = await anext(session_gen)

        try:
            # Build query
            statement = select(Task).where(Task.user_id == UUID(user_id))

            # Apply filters
            if completed is not None:
                statement = statement.where(Task.completed == completed)
            if priority:
                statement = statement.where(Task.priority == priority)
            if status:
                statement = statement.where(Task.status == status)
            if tag:
                # Filter by tag (JSON array contains)
                statement = statement.where(Task.tags.contains([tag]))

            # Apply sorting
            sort_field = getattr(Task, sort_by, Task.created_at)
            if sort_order == "asc":
                statement = statement.order_by(sort_field.asc())
            else:
                statement = statement.order_by(sort_field.desc())

            result = await session.execute(statement)
            tasks = result.scalars().all()

            return {
                "success": True,
                "count": len(tasks),
                "tasks": [
                    {
                        "id": str(task.id),
                        "title": task.title,
                        "description": task.description,
                        "priority": task.priority,
                        "status": task.status,
                        "completed": task.completed,
                        "tags": task.tags,
                        "due_date": task.due_date.isoformat() if task.due_date else None,
                        "recurrence_pattern": task.recurrence_pattern,
                        "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                        "created_at": task.created_at.isoformat(),
                        "updated_at": task.updated_at.isoformat()
                    }
                    for task in tasks
                ]
            }
        finally:
            await session.close()
    except Exception as e:
        return {"error": f"Failed to list tasks: {str(e)}", "success": False}


@mcp.tool()
async def update_task(
    user_id: str,
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    tags: Optional[List[str]] = None,
    due_date: Optional[str] = None,
    recurrence_pattern: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Update an existing task.

    Args:
        user_id: The UUID of the user
        task_id: The UUID of the task to update
        title: New title (optional)
        description: New description (optional)
        priority: New priority (optional)
        status: New status (optional)
        tags: New tags list (optional)
        due_date: New due date in ISO format (optional)
        recurrence_pattern: New recurrence pattern (optional)

    Returns:
        Dict containing the updated task details
    """
    try:
        # Parse due_date if provided
        parsed_due_date = None
        if due_date:
            try:
                parsed_due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            except ValueError:
                return {"error": f"Invalid due_date format: {due_date}", "success": False}

        session_gen = get_async_session()
        session = await anext(session_gen)

        try:
            # Find the task
            statement = select(Task).where(and_(Task.id == UUID(task_id), Task.user_id == UUID(user_id)))
            result = await session.execute(statement)
            db_task = result.scalar_one_or_none()

            if not db_task:
                return {"error": "Task not found", "success": False}

            # Update fields if provided
            if title is not None:
                if not title or title.strip() == "":
                    return {"error": "Title cannot be empty", "success": False}
                db_task.title = title.strip()
            if description is not None:
                db_task.description = description
            if priority is not None:
                db_task.priority = priority
            if status is not None:
                db_task.status = status
            if tags is not None:
                db_task.tags = tags
            if due_date is not None:
                db_task.due_date = parsed_due_date
            if recurrence_pattern is not None:
                db_task.recurrence_pattern = recurrence_pattern

            db_task.updated_at = datetime.utcnow()

            session.add(db_task)
            await session.commit()
            await session.refresh(db_task)

            return {
                "success": True,
                "task": {
                    "id": str(db_task.id),
                    "title": db_task.title,
                    "description": db_task.description,
                    "priority": db_task.priority,
                    "status": db_task.status,
                    "completed": db_task.completed,
                    "tags": db_task.tags,
                    "due_date": db_task.due_date.isoformat() if db_task.due_date else None,
                    "recurrence_pattern": db_task.recurrence_pattern,
                    "updated_at": db_task.updated_at.isoformat()
                }
            }
        finally:
            await session.close()
    except Exception as e:
        return {"error": f"Failed to update task: {str(e)}", "success": False}


@mcp.tool()
async def delete_task(user_id: str, task_id: str) -> Dict[str, Any]:
    """
    Delete a task.

    Args:
        user_id: The UUID of the user
        task_id: The UUID of the task to delete

    Returns:
        Dict containing success status and message
    """
    try:
        session_gen = get_async_session()
        session = await anext(session_gen)

        try:
            # Find the task
            statement = select(Task).where(and_(Task.id == UUID(task_id), Task.user_id == UUID(user_id)))
            result = await session.execute(statement)
            db_task = result.scalar_one_or_none()

            if not db_task:
                return {"error": "Task not found", "success": False}

            task_title = db_task.title
            await session.delete(db_task)
            await session.commit()

            return {
                "success": True,
                "message": f"Task '{task_title}' deleted successfully"
            }
        finally:
            await session.close()
    except Exception as e:
        return {"error": f"Failed to delete task: {str(e)}", "success": False}


@mcp.tool()
async def mark_complete(user_id: str, task_id: str, completed: bool = True) -> Dict[str, Any]:
    """
    Mark a task as complete or incomplete.

    Args:
        user_id: The UUID of the user
        task_id: The UUID of the task
        completed: True to mark complete, False to mark incomplete. Default: True

    Returns:
        Dict containing the updated task details
    """
    try:
        session_gen = get_async_session()
        session = await anext(session_gen)

        try:
            # Find the task
            statement = select(Task).where(and_(Task.id == UUID(task_id), Task.user_id == UUID(user_id)))
            result = await session.execute(statement)
            db_task = result.scalar_one_or_none()

            if not db_task:
                return {"error": "Task not found", "success": False}

            # Update completion status
            db_task.completed = completed
            db_task.status = "complete" if completed else "pending"
            db_task.completed_at = datetime.utcnow() if completed else None
            db_task.updated_at = datetime.utcnow()

            session.add(db_task)
            await session.commit()
            await session.refresh(db_task)

            return {
                "success": True,
                "task": {
                    "id": str(db_task.id),
                    "title": db_task.title,
                    "completed": db_task.completed,
                    "status": db_task.status,
                    "completed_at": db_task.completed_at.isoformat() if db_task.completed_at else None
                },
                "message": f"Task marked as {'complete' if completed else 'incomplete'}"
            }
        finally:
            await session.close()
    except Exception as e:
        return {"error": f"Failed to mark task: {str(e)}", "success": False}


# Run the MCP server
if __name__ == "__main__":
    mcp.run()
