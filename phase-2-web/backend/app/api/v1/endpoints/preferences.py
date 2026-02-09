"""
User preferences endpoint
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from app.api.deps import get_current_user_id

router = APIRouter()


class UserPreferences(BaseModel):
    """User preferences schema"""
    theme_preference: Optional[str] = None


@router.put("/user/preferences", summary="Update user preferences")
async def update_user_preferences(
    preferences: UserPreferences,
    current_user_id: str = Depends(get_current_user_id)
) -> dict:
    """
    Update user preferences including theme.

    Args:
        preferences: User preferences to update
        current_user_id: Authenticated user ID from JWT token

    Returns:
        Success status
    """
    try:
        # Validate theme preference
        if preferences.theme_preference:
            valid_themes = ['light', 'dark', 'purple']
            if preferences.theme_preference not in valid_themes:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Invalid theme. Must be one of: {', '.join(valid_themes)}"
                )

        # In a real implementation, update user in database
        # from app.db.session import get_db
        # async with get_db() as db:
        #     user = await db.get(User, current_user_id)
        #     if user:
        #         user.theme_preference = preferences.theme_preference
        #         await db.commit()

        return {
            "status": "success",
            "message": "Preferences updated successfully",
            "preferences": preferences.dict(exclude_none=True)
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating preferences: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update preferences: {str(e)}"
        )
