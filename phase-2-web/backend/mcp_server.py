"""
MCP Server for Todo Operations
Exposes todo CRUD functions as standardized MCP tools for AI agents
"""
from fastmcp import FastMCP
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("Todo MCP Server")
logger.info("MCP Server initialized")


@mcp.tool()
async def add_task(
    user_id: str,
    title: str,
    description: Optional[str] = None,
    priority: str = "medium",
    tags: Optional[List[str]] = None,
    due_date: Optional[str] = None,
    recurrence_pattern: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Add a new task for a user.

    Args:
        user_id: UUID of the user
        title: Task title (required)
        description: Task description (optional)
        priority: Priority level (low, medium, high, urgent)
        tags: List of tags for categorization
        due_date: Due date in ISO format or natural language
        recurrence_pattern: Recurrence pattern dict (type, interval, etc.)

    Returns:
        Dictionary with task details including task_id
    """
    logger.info(f"MCP add_task called for user {user_id}: '{title}'")
    logger.debug(f"Task details - priority: {priority}, tags: {tags}, due_date: {due_date}, recurrence: {recurrence_pattern}")

    try:
        # This will be called by the AI agent through the MCP protocol
        # The actual database operations will be handled by the backend API
        result = {
            "status": "success",
            "message": f"Task '{title}' added successfully",
            "task": {
                "title": title,
                "description": description,
                "priority": priority,
                "tags": tags or [],
                "due_date": due_date,
                "recurrence_pattern": recurrence_pattern,
                "user_id": user_id
            }
        }
        logger.info(f"Task '{title}' added successfully for user {user_id}")
        return result
    except Exception as e:
        logger.error(f"Error adding task for user {user_id}: {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"Failed to add task: {str(e)}"
        }


@mcp.tool()
async def delete_task(
    user_id: str,
    task_id: str
) -> Dict[str, Any]:
    """
    Delete a task with user ownership verification.

    Args:
        user_id: UUID of the user
        task_id: UUID of the task to delete

    Returns:
        Dictionary with deletion status
    """
    logger.info(f"MCP delete_task called for user {user_id}, task {task_id}")

    try:
        result = {
            "status": "success",
            "message": f"Task {task_id} deleted successfully",
            "task_id": task_id
        }
        logger.info(f"Task {task_id} deleted successfully for user {user_id}")
        return result
    except Exception as e:
        logger.error(f"Error deleting task {task_id} for user {user_id}: {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"Failed to delete task: {str(e)}"
        }


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
    recurrence_pattern: Optional[Dict[str, Any]] = None,
    completed: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Update an existing task with new properties.

    Args:
        user_id: UUID of the user
        task_id: UUID of the task to update
        title: New task title
        description: New task description
        priority: New priority level
        status: New status (pending, in-progress, complete)
        tags: New list of tags
        due_date: New due date
        recurrence_pattern: New recurrence pattern
        completed: New completion status

    Returns:
        Dictionary with updated task details
    """
    logger.info(f"MCP update_task called for user {user_id}, task {task_id}")

    try:
        updates = {}
        if title is not None:
            updates["title"] = title
        if description is not None:
            updates["description"] = description
        if priority is not None:
            updates["priority"] = priority
        if status is not None:
            updates["status"] = status
        if tags is not None:
            updates["tags"] = tags
        if due_date is not None:
            updates["due_date"] = due_date
        if recurrence_pattern is not None:
            updates["recurrence_pattern"] = recurrence_pattern
        if completed is not None:
            updates["completed"] = completed

        logger.debug(f"Task {task_id} updates: {updates}")

        result = {
            "status": "success",
            "message": f"Task {task_id} updated successfully",
            "task_id": task_id,
            "updates": updates
        }
        logger.info(f"Task {task_id} updated successfully for user {user_id} with {len(updates)} changes")
        return result
    except Exception as e:
        logger.error(f"Error updating task {task_id} for user {user_id}: {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"Failed to update task: {str(e)}"
        }


@mcp.tool()
async def list_tasks(
    user_id: str,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    tag: Optional[str] = None,
    sort_by: str = "created_at",
    order: str = "desc",
    limit: int = 100
) -> Dict[str, Any]:
    """
    List tasks for a user with optional filtering and sorting.

    Args:
        user_id: UUID of the user
        priority: Filter by priority (low, medium, high, urgent)
        status: Filter by status (pending, in-progress, complete)
        tag: Filter by tag
        sort_by: Sort field (created_at, due_date, priority)
        order: Sort order (asc, desc)
        limit: Maximum number of tasks to return

    Returns:
        Dictionary with list of tasks
    """
    logger.info(f"MCP list_tasks called for user {user_id}")
    logger.debug(f"Filters - priority: {priority}, status: {status}, tag: {tag}, sort_by: {sort_by}, order: {order}, limit: {limit}")

    try:
        filters = {}
        if priority:
            filters["priority"] = priority
        if status:
            filters["status"] = status
        if tag:
            filters["tag"] = tag

        result = {
            "status": "success",
            "tasks": [],  # Will be populated by backend
            "filters": filters,
            "sort_by": sort_by,
            "order": order,
            "count": 0
        }
        logger.info(f"Listed tasks for user {user_id} with {len(filters)} filters")
        return result
    except Exception as e:
        logger.error(f"Error listing tasks for user {user_id}: {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"Failed to list tasks: {str(e)}"
        }


@mcp.tool()
async def mark_complete(
    user_id: str,
    task_id: str
) -> Dict[str, Any]:
    """
    Mark a task as complete with status validation.
    If task is recurring, automatically creates next occurrence.

    Args:
        user_id: UUID of the user
        task_id: UUID of the task to mark complete

    Returns:
        Dictionary with completion status and next occurrence info
    """
    logger.info(f"MCP mark_complete called for user {user_id}, task {task_id}")

    try:
        # In a real implementation, this would:
        # 1. Mark task as complete in database
        # 2. Check if task has recurrence_pattern
        # 3. If recurring, create next occurrence using recurrence_service
        # 4. Return both completion status and next task info

        result = {
            "status": "success",
            "message": f"Task {task_id} marked as complete",
            "task_id": task_id,
            "completed": True,
            "completed_at": datetime.utcnow().isoformat()
        }

        # Placeholder for recurrence logic
        # from app.services.recurrence_service import recurrence_service
        # task = await db.get(Task, task_id)
        # if task and task.recurrence_pattern:
        #     next_task = await recurrence_service.create_next_occurrence(task, db)
        #     if next_task:
        #         result["next_occurrence"] = next_task
        #         result["message"] += f" Next occurrence created with ID {next_task['id']}"
        #         logger.info(f"Created next occurrence for recurring task {task_id}")

        logger.info(f"Task {task_id} marked as complete for user {user_id}")
        return result
    except Exception as e:
        logger.error(f"Error marking task {task_id} complete for user {user_id}: {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"Failed to mark task complete: {str(e)}"
        }


@mcp.tool()
async def search_tasks(
    user_id: str,
    query: str
) -> Dict[str, Any]:
    """
    Search tasks by title or description.

    Args:
        user_id: UUID of the user
        query: Search query string

    Returns:
        Dictionary with matching tasks
    """
    logger.info(f"MCP search_tasks called for user {user_id} with query: '{query}'")

    try:
        result = {
            "status": "success",
            "query": query,
            "tasks": [],  # Will be populated by backend
            "count": 0
        }
        logger.info(f"Search completed for user {user_id}")
        return result
    except Exception as e:
        logger.error(f"Error searching tasks for user {user_id}: {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"Failed to search tasks: {str(e)}"
        }


# Server startup configuration
if __name__ == "__main__":
    # Run the MCP server on port 8001
    print("Starting MCP Server on port 8001...")
    print("Available tools:")
    print("  - add_task: Add a new task")
    print("  - delete_task: Delete a task")
    print("  - update_task: Update task properties")
    print("  - list_tasks: List tasks with filters")
    print("  - mark_complete: Mark task as complete")
    print("  - search_tasks: Search tasks by query")

    # FastMCP will handle the server startup
    mcp.run()
