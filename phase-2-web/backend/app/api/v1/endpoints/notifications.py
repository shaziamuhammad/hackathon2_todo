"""
Notifications API endpoint
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from app.api.deps import get_current_user_id
from app.services.notification_service import notification_service

router = APIRouter()


@router.get("/notifications", summary="Get pending notifications for user")
async def get_notifications(
    current_user_id: str = Depends(get_current_user_id)
) -> Dict[str, Any]:
    """
    Retrieve all pending notifications for the authenticated user.

    Args:
        current_user_id: Authenticated user ID from JWT token

    Returns:
        Dictionary with list of pending notifications
    """
    try:
        notifications = await notification_service.get_pending_notifications(
            user_id=current_user_id
        )

        return {
            "status": "success",
            "notifications": notifications,
            "count": len(notifications)
        }

    except Exception as e:
        print(f"Error fetching notifications: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch notifications: {str(e)}"
        )


@router.post("/notifications/{notification_id}/mark-sent", summary="Mark notification as sent")
async def mark_notification_sent(
    notification_id: str,
    current_user_id: str = Depends(get_current_user_id)
) -> Dict[str, Any]:
    """
    Mark a notification as sent/read.

    Args:
        notification_id: Notification UUID
        current_user_id: Authenticated user ID from JWT token

    Returns:
        Success status
    """
    try:
        success = await notification_service.mark_notification_sent(notification_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )

        return {
            "status": "success",
            "message": "Notification marked as sent"
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error marking notification as sent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mark notification as sent: {str(e)}"
        )
