#!/usr/bin/env python3
"""
Check the actual running server configuration by examining the startup process
"""

import sys
import os

# Add the backend path to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'phase-2-web', 'backend'))

def check_server_startup():
    """Simulate the server startup process to see what happens"""

    print("Checking server startup process...")

    try:
        # Import and create the app exactly as uvicorn would
        from app.main import app
        from app.core.config import settings

        print(f"App created successfully")
        print(f"Settings loaded from: {settings.Config.env_file}")
        print(f"BACKEND_CORS_ORIGINS: {settings.BACKEND_CORS_ORIGINS}")

        # Check if the middleware is correctly added
        print(f"Number of user middlewares: {len(app.user_middleware)}")

        cors_middleware_found = False
        for i, middleware in enumerate(app.user_middleware):
            print(f"  Middleware {i}: {middleware.cls.__name__ if hasattr(middleware.cls, '__name__') else middleware.cls}")
            if 'CORSMiddleware' in str(middleware.cls):
                cors_middleware_found = True
                print(f"    Options: {middleware.options}")

        if cors_middleware_found:
            print("✓ CORSMiddleware is properly registered")
        else:
            print("✗ CORSMiddleware is NOT registered!")

        # Check the mounted routes
        print(f"\nMounted routes containing 'auth':")
        for route in app.routes:
            if hasattr(route, 'path') and 'auth' in route.path.lower():
                print(f"  {route.path} - Methods: {getattr(route, 'methods', 'N/A')}")

        # Let's also check if there's an issue with the API router mounting
        print(f"\nChecking API router mounting...")
        from app.api.api_v1.api import api_router

        print(f"API Router routes: {[r.path for r in api_router.routes if hasattr(r, 'path')]}")

        return True

    except Exception as e:
        print(f"Error during startup simulation: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_manual_cors_check():
    """Test the CORS configuration manually"""
    try:
        from app.core.config import settings
        print(f"\nManual CORS check:")
        print(f"RAW_ALLOWED_ORIGINS: {repr(settings.RAW_ALLOWED_ORIGINS)}")
        print(f"PARSED BACKEND_CORS_ORIGINS: {settings.BACKEND_CORS_ORIGINS}")

        # Test the parsing logic manually
        import json
        try:
            parsed = json.loads(settings.RAW_ALLOWED_ORIGINS)
            print(f"Parsed origins: {parsed}")
            print(f"Type: {type(parsed)}")
        except Exception as e:
            print(f"Failed to parse RAW_ALLOWED_ORIGINS: {e}")

        return True
    except Exception as e:
        print(f"Error in manual CORS check: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Analyzing server configuration for CORS issues...")
    print("="*60)

    success1 = check_server_startup()
    success2 = test_manual_cors_check()

    print("="*60)
    if success1 and success2:
        print("Server configuration analysis completed.")
        print("\nIf CORS is still not working despite correct configuration,")
        print("try running uvicorn with explicit reload and verbose options:")
        print("cd D:\\hackathon2_todo\\phase-2-web\\backend")
        print("uvicorn app.main:app --reload --port 8000 --log-level debug")
    else:
        print("Server configuration analysis failed.")