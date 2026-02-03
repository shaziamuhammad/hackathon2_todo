"""
TodoService for the Todo application.

Handles business logic for managing tasks in memory.
"""
from typing import List, Optional
from ..models.task import Task
import uuid
import logging
import sys


def setup_logging(level: str = "INFO") -> logging.Logger:
    """
    Set up logging for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger('todo_app')
    logger.setLevel(getattr(logging, level.upper()))

    # Avoid adding multiple handlers if logger already exists
    if logger.handlers:
        return logger

    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


class TodoService:
    """
    Service class for managing todo tasks in memory.

    Provides methods for adding, viewing, updating, deleting, and marking tasks
    as complete/incomplete.
    """

    def __init__(self):
        """Initialize the TodoService with an empty task list."""
        self._tasks: List[Task] = []
        self.logger = setup_logging()

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task to the todo list.

        Args:
            title: The title of the task
            description: The description of the task (optional)

        Returns:
            The newly created Task object

        Raises:
            ValueError: If title is empty
        """
        try:
            task_id = str(uuid.uuid4())
            task = Task(id=task_id, title=title, description=description, completed=False)
            self._tasks.append(task)
            self.logger.info(f"Task added with ID: {task_id}")
            return task
        except ValueError as e:
            self.logger.error(f"Failed to add task: {e}")
            raise

    def view_tasks(self) -> List[Task]:
        """
        Get all tasks in the todo list.

        Returns:
            A list of all Task objects
        """
        self.logger.info(f"Retrieved {len(self._tasks)} tasks")
        return self._tasks.copy()

    def update_task(self, task_id: str, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """
        Update an existing task by ID.

        Args:
            task_id: The ID of the task to update
            title: New title for the task (optional)
            description: New description for the task (optional)

        Returns:
            The updated Task object, or None if task not found
        """
        for task in self._tasks:
            if task.id == task_id:
                original_title = task.title
                if title is not None:
                    task.title = title
                if description is not None:
                    task.description = description
                self.logger.info(f"Task updated: {task_id} (title: '{original_title}' -> '{task.title}')")
                return task
        self.logger.warning(f"Attempted to update non-existent task: {task_id}")
        return None

    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if not found
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[i]
                self.logger.info(f"Task deleted: {task_id}")
                return True
        self.logger.warning(f"Attempted to delete non-existent task: {task_id}")
        return False

    def mark_task_complete(self, task_id: str) -> Optional[Task]:
        """
        Mark a task as complete.

        Args:
            task_id: The ID of the task to mark as complete

        Returns:
            The updated Task object, or None if task not found
        """
        for task in self._tasks:
            if task.id == task_id:
                task.completed = True
                self.logger.info(f"Task marked complete: {task_id}")
                return task
        self.logger.warning(f"Attempted to mark non-existent task as complete: {task_id}")
        return None

    def mark_task_incomplete(self, task_id: str) -> Optional[Task]:
        """
        Mark a task as incomplete.

        Args:
            task_id: The ID of the task to mark as incomplete

        Returns:
            The updated Task object, or None if task not found
        """
        for task in self._tasks:
            if task.id == task_id:
                task.completed = False
                self.logger.info(f"Task marked incomplete: {task_id}")
                return task
        self.logger.warning(f"Attempted to mark non-existent task as incomplete: {task_id}")
        return None

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task object if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None