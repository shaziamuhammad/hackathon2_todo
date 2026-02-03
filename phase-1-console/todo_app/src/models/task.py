"""
Task model for the Todo application.

Represents a single todo item with attributes: unique ID, title, description, and completion status.
"""
from dataclasses import dataclass
from typing import Optional
import uuid


@dataclass
class Task:
    """
    Represents a single todo task.

    Attributes:
        id: Unique identifier for the task
        title: Title of the task
        description: Description of the task (optional)
        completed: Boolean indicating if the task is completed
    """
    id: str
    title: str
    description: Optional[str] = ""
    completed: bool = False

    def __post_init__(self):
        """Validate the task after initialization."""
        if not self.title:
            raise ValueError("Task title cannot be empty")
        if not self.id:
            raise ValueError("Task ID cannot be empty")