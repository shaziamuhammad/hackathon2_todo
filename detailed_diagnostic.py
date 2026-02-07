#!/usr/bin/env python3
"""
Detailed diagnostic script to identify the exact issue with registration
"""

import sys
import os

# Add the backend directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'phase-2-web', 'backend'))

try:
    print("=== Detailed Registration Diagnostic ===\n")

    # 1. Check database connection
    print("1. Testing Database Connection...")
    from app.core.config import settings
    print(f"   - Database URL: {settings.DATABASE_URL[:50]}...")

    try:
        from app.db.session import engine
        import asyncio
        from sqlalchemy import text

        async def test_connection():
            async with engine.connect() as conn:
                result = await conn.execute(text("SELECT 1"))
                print("   - Database connection: [OK]")
                return True
    except Exception as e:
        print(f"   - Database connection: [ERROR] - {e}")

    # 2. Test the registration function directly
    print("\n2. Testing Registration Logic Directly...")
    from app.models.user import UserCreate
    from app.auth.utils import get_password_hash

    # Create a test user
    test_user = UserCreate(email="test@example.com", password="testpass123")
    print(f"   - Test user created: {test_user.email}")

    # Test password hashing
    try:
        hashed = get_password_hash(test_user.password)
        print("   - Password hashing: [OK]")
    except Exception as e:
        print(f"   - Password hashing: [ERROR] - {e}")

    # 3. Check the dependency injection
    print("\n3. Testing Dependency Injection...")
    from app.db.session import get_async_session
    try:
        # This will test if the dependency function is callable
        dep_gen = get_async_session()
        print("   - Async session dependency: [OK]")
    except Exception as e:
        print(f"   - Async session dependency: [ERROR] - {e}")

    # 4. Test FastAPI app startup
    print("\n4. Testing FastAPI App Startup...")
    from app.main import app
    print(f"   - App title: {app.title}")
    print(f"   - App version: {app.version}")

    # 5. Check if there are any startup dependencies
    print("\n5. Testing Lifespan Context...")
    try:
        # Check if lifespan function works
        from contextlib import asynccontextmanager
        print("   - Lifespan manager: [OK]")
    except Exception as e:
        print(f"   - Lifespan manager: [ERROR] - {e}")

    # 6. Check if we can import all required modules
    print("\n6. Testing Module Imports...")
    modules_to_check = [
        "app.auth.utils",
        "app.models.user",
        "app.db.session",
        "app.api.api_v1.endpoints.auth"
    ]

    for module in modules_to_check:
        try:
            __import__(module)
            print(f"   - {module}: [OK]")
        except Exception as e:
            print(f"   - {module}: [ERROR] - {e}")

    # 7. Check the specific register function signature
    print("\n7. Checking Register Function Signature...")
    try:
        from app.api.api_v1.endpoints.auth import register_user
        import inspect
        sig = inspect.signature(register_user)
        print(f"   - Function signature: {sig}")
        print("   - Register function: [OK]")
    except Exception as e:
        print(f"   - Register function: [ERROR] - {e}")

    print("\n=== Diagnostic Complete ===")
    print("If all tests show [OK], the issue might be at runtime or network level.")
    print("Consider checking:")
    print("- Actual database connectivity when the server runs")
    print("- Network connectivity between frontend and backend")
    print("- Whether the backend server is accessible at http://localhost:8000")

except Exception as e:
    print(f"[CRITICAL ERROR] {e}")
    import traceback
    traceback.print_exc()