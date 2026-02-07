import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings

async def test_db_connection():
    print("Testing database connection...")
    print(f"Database URL: {settings.DATABASE_URL}")

    try:
        engine = create_async_engine(settings.DATABASE_URL)

        # Test the connection
        async with engine.connect() as conn:
            result = await conn.execute("SELECT 1")
            print("✅ Database connection successful!")
            print(f"Result: {result.fetchone()}")

    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Dispose of the engine
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_db_connection())