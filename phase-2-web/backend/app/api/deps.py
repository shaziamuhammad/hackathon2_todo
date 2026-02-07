from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.jwt_handler import get_user_id_from_token
from app.database import get_db
from sqlalchemy.orm import Session


security = HTTPBearer()


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """
    Get current user ID from JWT token
    """
    token = credentials.credentials
    user_id = get_user_id_from_token(token)
    return user_id


def verify_user_owns_resource(token_user_id: int, url_user_id: int):
    """
    Verify that the user ID from the token matches the user ID in the URL
    """
    if token_user_id != url_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )


def get_db_session():
    """
    Get database session dependency
    """
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()