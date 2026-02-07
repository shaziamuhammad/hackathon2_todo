from sqlmodel import SQLModel
from app.models.user import User
from app.models.task import Task
from app.db.session import engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


async def init_db():
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)