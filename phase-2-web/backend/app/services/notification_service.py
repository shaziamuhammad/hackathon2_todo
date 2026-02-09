"""
Notification Service
Manages notification scheduling and delivery
"""
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import uuid


class NotificationService:
    """Service for managing task notifications"""

    def __init__(self):
        """Initialize notification service"""
        self.pending_notifications = {}  # In-memory store (use database in production)

    async def schedule_notification(
        self,
        task_id: str,
        user_id: str,
        task_title: str,
        due_date: datetime,
        notification_type: str = "due_date"
    ) -> Dict[str, Any]:
        """
        Schedule a notification for a task.

        Args:
            task_id: Task UUID
            user_id: User UUID
            task_title: Task title
            due_date: When the task is due
            notification_type: Type of notification (due_date, reminder, etc.)

        Returns:
            Notification details
        """
        notification_id = str(uuid.uuid4())

        # Calculate notification time (1 hour before due date)
        notification_time = due_date - timedelta(hours=1)

        notification = {
            "id": notification_id,
            "task_id": task_id,
            "user_id": user_id,
            "title": task_title,
            "message": f"Task '{task_title}' is due soon!",
            "notification_type": notification_type,
            "scheduled_for": notification_time.isoformat(),
            "sent": False,
            "created_at": datetime.utcnow().isoformat()
        }

        # Store notification (in production, save to database)
        self.pending_notifications[notification_id] = notification

        # Schedule with scheduler
        from app.services.scheduler import scheduler
        scheduler.schedule_task_notification(
            task_id=task_id,
            user_id=user_id,
            due_date=due_date,
            title=task_title
        )

        return notification

    async def get_pending_notifications(
        self,
        user_id: str
    ) -> List[Dict[str, Any]]:
        """
        Get all pending notifications for a user.

        Args:
            user_id: User UUID

        Returns:
            List of pending notifications
        """
        # In production, query from database
        user_notifications = [
            notif for notif in self.pending_notifications.values()
            if notif["user_id"] == user_id and not notif["sent"]
        ]

        return user_notifications

    async def mark_notification_sent(
        self,
        notification_id: str
    ) -> bool:
        """
        Mark a notification as sent.

        Args:
            notification_id: Notification UUID

        Returns:
            True if successful, False otherwise
        """
        if notification_id in self.pending_notifications:
            self.pending_notifications[notification_id]["sent"] = True
            self.pending_notifications[notification_id]["sent_at"] = datetime.utcnow().isoformat()
            return True
        return False

    async def send_notification(
        self,
        user_id: str,
        task_id: str,
        title: str,
        message: str
    ) -> Dict[str, Any]:
        """
        Send a notification to a user.

        Args:
            user_id: User UUID
            task_id: Task UUID
            title: Notification title
            message: Notification message

        Returns:
            Notification result
        """
        # In production, this would:
        # 1. Send browser push notification
        # 2. Send email notification
        # 3. Send SMS notification (if configured)
        # 4. Store notification in database

        notification = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "task_id": task_id,
            "title": title,
            "message": message,
            "sent": True,
            "sent_at": datetime.utcnow().isoformat()
        }

        print(f"Notification sent to user {user_id}: {message}")

        return notification

    async def cancel_notification(
        self,
        task_id: str
    ) -> bool:
        """
        Cancel scheduled notifications for a task.

        Args:
            task_id: Task UUID

        Returns:
            True if successful, False otherwise
        """
        # Remove from pending notifications
        notifications_to_remove = [
            notif_id for notif_id, notif in self.pending_notifications.items()
            if notif["task_id"] == task_id and not notif["sent"]
        ]

        for notif_id in notifications_to_remove:
            del self.pending_notifications[notif_id]

        # Cancel scheduled job
        from app.services.scheduler import scheduler
        try:
            scheduler.scheduler.remove_job(f"notification_{task_id}")
        except Exception:
            pass

        return len(notifications_to_remove) > 0


# Create singleton instance
notification_service = NotificationService()
