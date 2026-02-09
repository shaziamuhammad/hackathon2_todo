"""
Recurrence Service
Handles recurring task logic and auto-rescheduling
"""
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import Dict, Any, Optional
import uuid


class RecurrenceService:
    """Service for managing recurring tasks"""

    @staticmethod
    def calculate_next_occurrence(
        current_date: datetime,
        recurrence_pattern: Dict[str, Any]
    ) -> Optional[datetime]:
        """
        Calculate the next occurrence date based on recurrence pattern.

        Args:
            current_date: Current task date
            recurrence_pattern: Recurrence pattern dict with type, interval, etc.

        Returns:
            Next occurrence datetime or None if pattern is invalid
        """
        if not recurrence_pattern or "type" not in recurrence_pattern:
            return None

        pattern_type = recurrence_pattern.get("type")
        interval = recurrence_pattern.get("interval", 1)

        try:
            if pattern_type == "daily":
                return current_date + timedelta(days=interval)

            elif pattern_type == "weekly":
                days_of_week = recurrence_pattern.get("days_of_week")
                if days_of_week:
                    # Find next occurrence on specified days of week
                    next_date = current_date + timedelta(days=1)
                    while next_date.weekday() not in days_of_week:
                        next_date += timedelta(days=1)
                    return next_date
                else:
                    # Simple weekly recurrence
                    return current_date + timedelta(weeks=interval)

            elif pattern_type == "monthly":
                day_of_month = recurrence_pattern.get("day_of_month")
                if day_of_month:
                    # Specific day of month
                    next_date = current_date + relativedelta(months=interval)
                    try:
                        next_date = next_date.replace(day=day_of_month)
                    except ValueError:
                        # Handle invalid day (e.g., Feb 31)
                        next_date = next_date.replace(day=1) + relativedelta(months=1) - timedelta(days=1)
                    return next_date
                else:
                    # Same day next month
                    return current_date + relativedelta(months=interval)

            elif pattern_type == "yearly":
                return current_date + relativedelta(years=interval)

            else:
                return None

        except Exception as e:
            print(f"Error calculating next occurrence: {e}")
            return None

    @staticmethod
    def should_reschedule(
        task_completed_at: datetime,
        recurrence_pattern: Dict[str, Any]
    ) -> bool:
        """
        Determine if a task should be rescheduled based on completion time.

        Args:
            task_completed_at: When the task was completed
            recurrence_pattern: Recurrence pattern dict

        Returns:
            True if task should be rescheduled, False otherwise
        """
        if not recurrence_pattern:
            return False

        # Check if recurrence has an end date
        ends_on = recurrence_pattern.get("ends_on")
        if ends_on:
            try:
                end_date = datetime.fromisoformat(ends_on) if isinstance(ends_on, str) else ends_on
                if task_completed_at >= end_date:
                    return False
            except (ValueError, TypeError):
                pass

        return True

    @staticmethod
    async def create_next_occurrence(
        original_task: Dict[str, Any],
        db_session: Any
    ) -> Optional[Dict[str, Any]]:
        """
        Create the next occurrence of a recurring task.

        Args:
            original_task: Original task data
            db_session: Database session

        Returns:
            New task data or None if creation failed
        """
        recurrence_pattern = original_task.get("recurrence_pattern")
        if not recurrence_pattern:
            return None

        # Calculate next due date
        current_due_date = original_task.get("due_date")
        if not current_due_date:
            current_due_date = datetime.utcnow()
        elif isinstance(current_due_date, str):
            current_due_date = datetime.fromisoformat(current_due_date)

        next_due_date = RecurrenceService.calculate_next_occurrence(
            current_due_date,
            recurrence_pattern
        )

        if not next_due_date:
            return None

        # Check if we should reschedule
        if not RecurrenceService.should_reschedule(datetime.utcnow(), recurrence_pattern):
            return None

        # Create new task with same properties but new due date
        new_task = {
            "id": str(uuid.uuid4()),
            "title": original_task.get("title"),
            "description": original_task.get("description"),
            "priority": original_task.get("priority", "medium"),
            "status": "pending",
            "tags": original_task.get("tags", []),
            "due_date": next_due_date.isoformat(),
            "recurrence_pattern": recurrence_pattern,
            "user_id": original_task.get("user_id"),
            "completed": False,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

        # In a real implementation, save to database
        # db_task = Task(**new_task)
        # db_session.add(db_task)
        # await db_session.commit()

        return new_task

    @staticmethod
    def get_recurrence_description(recurrence_pattern: Dict[str, Any]) -> str:
        """
        Generate human-readable description of recurrence pattern.

        Args:
            recurrence_pattern: Recurrence pattern dict

        Returns:
            Human-readable description
        """
        if not recurrence_pattern:
            return "No recurrence"

        pattern_type = recurrence_pattern.get("type")
        interval = recurrence_pattern.get("interval", 1)

        if pattern_type == "daily":
            if interval == 1:
                return "Daily"
            return f"Every {interval} days"

        elif pattern_type == "weekly":
            days_of_week = recurrence_pattern.get("days_of_week")
            if days_of_week:
                day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                days_str = ", ".join([day_names[d] for d in days_of_week if 0 <= d < 7])
                return f"Weekly on {days_str}"
            if interval == 1:
                return "Weekly"
            return f"Every {interval} weeks"

        elif pattern_type == "monthly":
            if interval == 1:
                return "Monthly"
            return f"Every {interval} months"

        elif pattern_type == "yearly":
            if interval == 1:
                return "Yearly"
            return f"Every {interval} years"

        return "Custom recurrence"


# Create singleton instance
recurrence_service = RecurrenceService()
