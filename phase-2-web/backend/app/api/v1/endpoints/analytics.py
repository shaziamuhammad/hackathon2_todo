"""
Task analytics and statistics endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List
from uuid import UUID
from datetime import datetime, timedelta

from app.models.task import Task
from app.auth.middleware import get_current_user_id
from app.db.session import get_async_session

router = APIRouter()


@router.get("/analytics/overview")
async def get_analytics_overview(
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
) -> Dict[str, Any]:
    """
    Get overview analytics for user's tasks.

    Returns:
        - Total tasks
        - Completed tasks
        - Pending tasks
        - Overdue tasks
        - Tasks by priority
        - Tasks by status
        - Completion rate
    """
    try:
        user_uuid = UUID(current_user_id)

        # Total tasks
        total_stmt = select(func.count(Task.id)).where(Task.user_id == user_uuid)
        total_result = await session.execute(total_stmt)
        total_tasks = total_result.scalar() or 0

        # Completed tasks
        completed_stmt = select(func.count(Task.id)).where(
            and_(Task.user_id == user_uuid, Task.completed == True)
        )
        completed_result = await session.execute(completed_stmt)
        completed_tasks = completed_result.scalar() or 0

        # Pending tasks
        pending_tasks = total_tasks - completed_tasks

        # Overdue tasks
        now = datetime.utcnow()
        overdue_stmt = select(func.count(Task.id)).where(
            and_(
                Task.user_id == user_uuid,
                Task.completed == False,
                Task.due_date < now
            )
        )
        overdue_result = await session.execute(overdue_stmt)
        overdue_tasks = overdue_result.scalar() or 0

        # Tasks by priority
        priority_stmt = select(Task.priority, func.count(Task.id)).where(
            Task.user_id == user_uuid
        ).group_by(Task.priority)
        priority_result = await session.execute(priority_stmt)
        tasks_by_priority = {row[0]: row[1] for row in priority_result.all()}

        # Tasks by status
        status_stmt = select(Task.status, func.count(Task.id)).where(
            Task.user_id == user_uuid
        ).group_by(Task.status)
        status_result = await session.execute(status_stmt)
        tasks_by_status = {row[0]: row[1] for row in status_result.all()}

        # Completion rate
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "overdue_tasks": overdue_tasks,
            "completion_rate": round(completion_rate, 2),
            "tasks_by_priority": tasks_by_priority,
            "tasks_by_status": tasks_by_status
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving analytics: {str(e)}"
        )


@router.get("/analytics/productivity")
async def get_productivity_stats(
    days: int = 7,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
) -> Dict[str, Any]:
    """
    Get productivity statistics for the last N days.

    Args:
        days: Number of days to analyze (default: 7)

    Returns:
        - Tasks completed per day
        - Tasks created per day
        - Average completion time
        - Most productive day
    """
    try:
        user_uuid = UUID(current_user_id)
        start_date = datetime.utcnow() - timedelta(days=days)

        # Tasks completed in period
        completed_stmt = select(Task).where(
            and_(
                Task.user_id == user_uuid,
                Task.completed == True,
                Task.completed_at >= start_date
            )
        )
        completed_result = await session.execute(completed_stmt)
        completed_tasks = completed_result.scalars().all()

        # Tasks created in period
        created_stmt = select(Task).where(
            and_(
                Task.user_id == user_uuid,
                Task.created_at >= start_date
            )
        )
        created_result = await session.execute(created_stmt)
        created_tasks = created_result.scalars().all()

        # Calculate daily stats
        daily_completed = {}
        daily_created = {}

        for task in completed_tasks:
            if task.completed_at:
                day = task.completed_at.date().isoformat()
                daily_completed[day] = daily_completed.get(day, 0) + 1

        for task in created_tasks:
            day = task.created_at.date().isoformat()
            daily_created[day] = daily_created.get(day, 0) + 1

        # Calculate average completion time
        completion_times = []
        for task in completed_tasks:
            if task.completed_at and task.created_at:
                time_diff = (task.completed_at - task.created_at).total_seconds() / 3600  # hours
                completion_times.append(time_diff)

        avg_completion_time = sum(completion_times) / len(completion_times) if completion_times else 0

        # Find most productive day
        most_productive_day = max(daily_completed.items(), key=lambda x: x[1]) if daily_completed else (None, 0)

        return {
            "period_days": days,
            "total_completed": len(completed_tasks),
            "total_created": len(created_tasks),
            "daily_completed": daily_completed,
            "daily_created": daily_created,
            "avg_completion_time_hours": round(avg_completion_time, 2),
            "most_productive_day": {
                "date": most_productive_day[0],
                "tasks_completed": most_productive_day[1]
            } if most_productive_day[0] else None
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving productivity stats: {str(e)}"
        )


@router.get("/analytics/upcoming")
async def get_upcoming_tasks(
    days: int = 7,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
) -> Dict[str, Any]:
    """
    Get tasks due in the next N days.

    Args:
        days: Number of days to look ahead (default: 7)

    Returns:
        - Tasks due today
        - Tasks due this week
        - Tasks due by priority
    """
    try:
        user_uuid = UUID(current_user_id)
        now = datetime.utcnow()
        end_date = now + timedelta(days=days)

        # Get upcoming tasks
        stmt = select(Task).where(
            and_(
                Task.user_id == user_uuid,
                Task.completed == False,
                Task.due_date.isnot(None),
                Task.due_date >= now,
                Task.due_date <= end_date
            )
        ).order_by(Task.due_date.asc())

        result = await session.execute(stmt)
        upcoming_tasks = result.scalars().all()

        # Categorize by timeframe
        today_end = now.replace(hour=23, minute=59, second=59)
        tasks_today = []
        tasks_this_week = []

        for task in upcoming_tasks:
            task_dict = {
                "id": str(task.id),
                "title": task.title,
                "priority": task.priority,
                "due_date": task.due_date.isoformat(),
                "status": task.status
            }

            if task.due_date <= today_end:
                tasks_today.append(task_dict)
            tasks_this_week.append(task_dict)

        # Group by priority
        by_priority = {}
        for task in upcoming_tasks:
            priority = task.priority
            if priority not in by_priority:
                by_priority[priority] = []
            by_priority[priority].append({
                "id": str(task.id),
                "title": task.title,
                "due_date": task.due_date.isoformat()
            })

        return {
            "period_days": days,
            "total_upcoming": len(upcoming_tasks),
            "due_today": tasks_today,
            "due_this_period": tasks_this_week,
            "by_priority": by_priority
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving upcoming tasks: {str(e)}"
        )
