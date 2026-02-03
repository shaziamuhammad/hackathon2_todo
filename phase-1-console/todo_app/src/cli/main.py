"""
Main CLI interface for the Todo application.
"""
import sys
import argparse
from typing import Optional
from ..services.todo_service import TodoService
import logging


class TodoCLI:
    """Command-line interface for the Todo application."""

    def __init__(self):
        """Initialize the CLI with a TodoService instance."""
        self.service = TodoService()
        self.logger = logging.getLogger('todo_app')

    def run(self):
        """Run the main CLI loop."""
        parser = argparse.ArgumentParser(description='Todo Application')
        subparsers = parser.add_subparsers(dest='command', help='Available commands')

        # Add task command
        add_parser = subparsers.add_parser('add', help='Add a new task')
        add_parser.add_argument('title', help='Title of the task')
        add_parser.add_argument('--description', '-d', default='', help='Description of the task')

        # List tasks command
        list_parser = subparsers.add_parser('list', help='List all tasks')

        # Update task command
        update_parser = subparsers.add_parser('update', help='Update a task')
        update_parser.add_argument('id', help='ID of the task to update')
        update_parser.add_argument('--title', help='New title for the task')
        update_parser.add_argument('--description', '-d', help='New description for the task')

        # Delete task command
        delete_parser = subparsers.add_parser('delete', help='Delete a task')
        delete_parser.add_argument('id', help='ID of the task to delete')

        # Mark task complete command
        complete_parser = subparsers.add_parser('complete', help='Mark a task as complete')
        complete_parser.add_argument('id', help='ID of the task to mark complete')

        # Mark task incomplete command
        incomplete_parser = subparsers.add_parser('incomplete', help='Mark a task as incomplete')
        incomplete_parser.add_argument('id', help='ID of the task to mark incomplete')

        # Parse arguments
        args = parser.parse_args()

        # Execute the appropriate command
        if args.command == 'add':
            self.add_task(args.title, args.description)
        elif args.command == 'list':
            self.list_tasks()
        elif args.command == 'update':
            self.update_task(args.id, args.title, args.description)
        elif args.command == 'delete':
            self.delete_task(args.id)
        elif args.command == 'complete':
            self.mark_task_complete(args.id)
        elif args.command == 'incomplete':
            self.mark_task_incomplete(args.id)
        else:
            parser.print_help()

    def add_task(self, title: str, description: str):
        """Add a new task."""
        try:
            task = self.service.add_task(title, description)
            print(f"Task added successfully!")
            print(f"ID: {task.id}")
            print(f"Title: {task.title}")
            print(f"Description: {task.description}")
            print(f"Status: {'Completed' if task.completed else 'Incomplete'}")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            self.logger.error(f"Failed to add task: {e}")

    def list_tasks(self):
        """List all tasks."""
        tasks = self.service.view_tasks()
        if not tasks:
            print("No tasks found.")
            return

        print(f"Total tasks: {len(tasks)}")
        for task in tasks:
            status = "✓" if task.completed else "○"
            print(f"[{status}] ID: {task.id}")
            print(f"    Title: {task.title}")
            print(f"    Description: {task.description}")
            print()

    def update_task(self, task_id: str, title: Optional[str], description: Optional[str]):
        """Update a task."""
        task = self.service.update_task(task_id, title, description)
        if task:
            print(f"Task updated successfully!")
            print(f"ID: {task.id}")
            print(f"Title: {task.title}")
            print(f"Description: {task.description}")
        else:
            print(f"Error: Task with ID '{task_id}' not found.", file=sys.stderr)
            self.logger.warning(f"Failed to update task: {task_id}")

    def delete_task(self, task_id: str):
        """Delete a task."""
        success = self.service.delete_task(task_id)
        if success:
            print(f"Task with ID '{task_id}' deleted successfully!")
        else:
            print(f"Error: Task with ID '{task_id}' not found.", file=sys.stderr)
            self.logger.warning(f"Failed to delete task: {task_id}")

    def mark_task_complete(self, task_id: str):
        """Mark a task as complete."""
        task = self.service.mark_task_complete(task_id)
        if task:
            print(f"Task '{task.title}' marked as complete!")
        else:
            print(f"Error: Task with ID '{task_id}' not found.", file=sys.stderr)
            self.logger.warning(f"Failed to mark task as complete: {task_id}")

    def mark_task_incomplete(self, task_id: str):
        """Mark a task as incomplete."""
        task = self.service.mark_task_incomplete(task_id)
        if task:
            print(f"Task '{task.title}' marked as incomplete!")
        else:
            print(f"Error: Task with ID '{task_id}' not found.", file=sys.stderr)
            self.logger.warning(f"Failed to mark task as incomplete: {task_id}")


def main():
    """Main entry point for the application."""
    cli = TodoCLI()
    cli.run()


# if __name__ == "__main__":
#     main()
if __name__ == "__main__":
    # Run interactive CLI directly (bypass argparse)
    cli = TodoCLI()
    cli.run()