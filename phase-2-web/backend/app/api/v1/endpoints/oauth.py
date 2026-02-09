"""
OAuth authentication endpoint
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import httpx
from datetime import datetime, timedelta
from jose import jwt
from app.config import config

router = APIRouter()


class OAuthRequest(BaseModel):
    """OAuth authentication request"""
    provider: str
    access_token: str
    id_token: Optional[str] = None
    email: str
    name: Optional[str] = None


@router.post("/auth/oauth", summary="Verify OAuth token and create/login user")
async def oauth_login(request: OAuthRequest) -> dict:
    """
    Verify OAuth token from provider and create/login user.

    Args:
        request: OAuth request with provider and tokens

    Returns:
        JWT access token and user info
    """
    try:
        # Verify token with provider
        user_info = None

        if request.provider == 'google':
            user_info = await verify_google_token(request.id_token or request.access_token)
        elif request.provider == 'facebook':
            user_info = await verify_facebook_token(request.access_token)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported OAuth provider: {request.provider}"
            )

        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid OAuth token"
            )

        # Check if user exists in database
        # In a real implementation:
        # user = await db.query(User).filter(User.email == user_info['email']).first()
        # if not user:
        #     user = User(
        #         email=user_info['email'],
        #         name=user_info.get('name'),
        #         provider=request.provider,
        #         provider_id=user_info.get('sub')
        #     )
        #     db.add(user)
        #     await db.commit()

        # Generate JWT token
        access_token = create_access_token(
            data={"sub": user_info['email'], "user_id": "mock-user-id"}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": "mock-user-id",
            "email": user_info['email'],
            "name": user_info.get('name')
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"OAuth error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OAuth authentication failed: {str(e)}"
        )


async def verify_google_token(token: str) -> Optional[dict]:
    """Verify Google OAuth token"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
            )

            if response.status_code == 200:
                return response.json()

        return None
    except Exception as e:
        print(f"Google token verification error: {e}")
        return None


async def verify_facebook_token(token: str) -> Optional[dict]:
    """Verify Facebook OAuth token"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://graph.facebook.com/me?access_token={token}&fields=id,name,email"
            )

            if response.status_code == 200:
                return response.json()

        return None
    except Exception as e:
        print(f"Facebook token verification error: {e}")
        return None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        config.SECRET_KEY,
        algorithm=config.ALGORITHM
    )

    return encoded_jwt
