# phase-2-web\backend\app\api\api_v1\endpoints\auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.models.user import User, UserCreate, UserRead, LoginRequest  # Import LoginRequest
from app.auth.utils import verify_password, get_password_hash, create_access_token
from datetime import timedelta
from typing import Annotated
import logging
from fastapi.responses import Response
from pydantic import BaseModel 

# Create the logger
logger = logging.getLogger("uvicorn")

router = APIRouter()




class RegisterResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead


@router.post("/register", response_model=RegisterResponse)
async def register_user(user_create: UserCreate, session=Depends(get_async_session)):
    logger.info("POST request received at /register endpoint")

    try:
        # Validate password length for bcrypt 72-byte limit
        if len(user_create.password.encode('utf-8')) > 72:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be 72 bytes or less when encoded as UTF-8"
            )

        if len(user_create.password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 6 characters long"
            )

        # Check if user already exists
        statement = select(User).where(User.email == user_create.email)
        result = await session.execute(statement)
        existing_user = result.first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        # Hash the password
        hashed_password = get_password_hash(user_create.password)

        # Create the new user
        db_user = User(
            email=user_create.email,
            hashed_password=hashed_password
        )

        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)

        # Create access token
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": str(db_user.id)}, expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": db_user
        }
    except Exception as e:
        # Log the error for debugging
        logger.error(f"Registration error: {str(e)}")
        raise


@router.post("/login")
async def login_user(login_request: LoginRequest, session=Depends(get_async_session)):
    try:
        email = login_request.email
        password = login_request.password

        # Validate password length for bcrypt 72-byte limit
        if len(password.encode('utf-8')) > 72:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be 72 bytes or less when encoded as UTF-8"
            )

        # Find user by email
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        db_user = result.scalar_one_or_none()

        if not db_user or not verify_password(password, db_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": str(db_user.id)}, expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": db_user
        }
    except Exception as e:
        # Log the error for debugging
        logger.error(f"Login error: {str(e)}")
        raise
