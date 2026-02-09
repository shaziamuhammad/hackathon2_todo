"""
Background Job Scheduler
Handles scheduled tasks like recurring task generation and notifications
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
from typing import Optional
import asyncio


class TaskScheduler:
    """Background scheduler for recurring tasks and notifications"""

    def __init__(self):
        """Initialize the scheduler"""
        self.scheduler = AsyncIOScheduler()
        self.is_running = False

    def start(self):
        """Start the background scheduler"""
        if not self.is_running:
            self.scheduler.start()
            self.is_running = True
            print("Task scheduler started")

            # Schedule recurring task check every hour
            self.scheduler.add_job(
                self.check_recurring_tasks,
                trigger=IntervalTrigger(hours=1),
                id="recurring_tasks_check",
                replace_existing=True
            )

            # Schedule notification check every 5 minutes
            self.scheduler.add_job(
                self.check_notifications,
                trigger=IntervalTrigger(minutes=5),
                id="notifications_check",
                replace_existing=True
            )

    def stop(self):
        """Stop the background scheduler"""
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            print("Task scheduler stopped")

    async def check_recurring_tasks(self):
        """
        Check for completed recurring tasks and create next occurrences.
        This runs periodically to ensure recurring tasks are regenerated.
        """
        try:
            print(f"[{datetime.now()}] Checking for recurring tasks to regenerate...")

            # In a real implementation:
            # 1. Query database for completed tasks with recurrence_pattern
            # 2. For each task, check if next occurrence should be created
            # 3. Use recurrence_service.create_next_occurrence()
            # 4. Save new task to database

            # Placeholder for actual implementation
            # from app.services.recurrence_service import recurrence_service
            # from app.db.session import get_db
            # async with get_db() as db:
            #     completed_recurring_tasks = await db.query(Task).filter(
            #         Task.completed == True,
            #         Task.recurrence_pattern != None
            #     ).all()
            #
            #     for task in completed_recurring_tasks:
            #         await recurrence_service.create_next_occurrence(task, db)

        except Exception as e:
            print(f"Error checking recurring tasks: {e}")

    async def check_notifications(self):
        """
        Check for tasks with upcoming due dates and schedule notifications.
        This runs periodically to ensure users are notified about due tasks.
        """
        try:
            print(f"[{datetime.now()}] Checking for tasks requiring notifications...")

            # In a real implementation:
            # 1. Query database for tasks with due_date in next 24 hours
            # 2. Check if notification already sent
            # 3. Create notification record
            # 4. Send notification via notification_service

            # Placeholder for actual implementation
            # from app.services.notification_service import notification_service
            # from app.db.session import get_db
            # async with get_db() as db:
            #     upcoming_tasks = await db.query(Task).filter(
            #         Task.due_date >= datetime.utcnow(),
            #         Task.due_date <= datetime.utcnow() + timedelta(hours=24),
            #         Task.completed == False
            #     ).all()
            #
            #     for task in upcoming_tasks:
            #         await notification_service.schedule_notification(task, db)

        except Exception as e:
            print(f"Error checking notifications: {e}")

    def schedule_task_notification(
        self,
        task_id: str,
        user_id: str,
        due_date: datetime,
        title: str
    ):
        """
        Schedule a notification for a specific task.

        Args:
            task_id: Task UUID
            user_id: User UUID
            due_date: When the task is due
            title: Task title
        """
        # Schedule notification 1 hour before due date
        notification_time = due_date - timedelta(hours=1)

        if notification_time > datetime.utcnow():
            self.scheduler.add_job(
                self.send_task_notification,
                trigger='date',
                run_date=notification_time,
                args=[task_id, user_id, title],
                id=f"notification_{task_id}",
                replace_existing=True
            )
            print(f"Scheduled notification for task {task_id} at {notification_time}")

    async def send_task_notification(self, task_id: str, user_id: str, title: str):
        """
        Send notification for a task.

        Args:
            task_id: Task UUID
            user_id: User UUID
            title: Task title
        """
        try:
            print(f"Sending notification for task: {title}")

            # In a real implementation:
            # 1. Create notification record in database
            # 2. Send via notification service (email, push, etc.)
            # 3. Mark notification as sent

            # Placeholder for actual implementation
            # from app.services.notification_service import notification_service
            # await notification_service.send_notification(
            #     user_id=user_id,
            #     task_id=task_id,
            #     title=title,
            #     message=f"Task '{title}' is due soon!"
            # )

        except Exception as e:
            print(f"Error sending notification: {e}")


# Create singleton instance
scheduler = TaskScheduler()
