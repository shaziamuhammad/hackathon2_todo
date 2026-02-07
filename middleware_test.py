#!/usr/bin/env python3
"""
Test script to check middleware configuration
"""

import sys
import os

# Add the backend path to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'phase-2-web', 'backend'))

def check_middleware_config():
    """Check the middleware configuration in detail"""

    print("Checking middleware configuration...")

    try:
        from app.main import app

        print(f"App title: {app.title}")
        print(f"App version: {app.version}")

        print(f"\nTotal middlewares: {len(app.user_middleware)}")

        for i, middleware in enumerate(app.user_middleware):
            print(f"Middleware {i}: {middleware.cls}")
            if hasattr(middleware, 'options'):
                print(f"  Options: {middleware.options}")

        # Check for CORSMiddleware specifically
        cors_middleware = None
        for middleware in app.middleware_stack.__dict__.get('_obj', app.middleware_stack).__dict__.get('_obj', app.middleware_stack).__dict__.get('app', app.middleware_stack):
            if hasattr(middleware, '__class__') and 'CORSMiddleware' in middleware.__class__.__name__:
                cors_middleware = middleware
                break

        if cors_middleware:
            print(f"\nFound CORSMiddleware: {cors_middleware}")
        else:
            print("\nCORSMiddleware not found in active middleware stack")

        # Let's also check the middleware stack more directly
        print(f"\nChecking middleware stack...")

        # Access the middleware stack more directly
        import inspect
        if hasattr(app, 'user_middleware'):
            print(f"User middlewares: {[(m.cls.__name__ if hasattr(m.cls, '__name__') else str(m.cls)) for m in app.user_middleware]}")

        # Check if CORSMiddleware is properly configured
        from fastapi.middleware.cors import CORSMiddleware
        cors_found = False
        for middleware in app.user_middleware:
            if middleware.cls == CORSMiddleware:
                cors_found = True
                print(f"✓ Found CORSMiddleware in user_middleware: {middleware.options}")
                break

        if not cors_found:
            print("✗ CORSMiddleware not found in user_middleware")
            print("Possible issue with middleware registration")

        return True

    except Exception as e:
        print(f"Error checking middleware: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_app_state():
    """Check the overall app state"""
    try:
        from app.main import app
        from app.core.config import settings

        print(f"\nConfiguration check:")
        print(f"API_V1_STR: {settings.API_V1_STR}")
        print(f"BACKEND_CORS_ORIGINS: {settings.BACKEND_CORS_ORIGINS}")

        print(f"\nApp routes count: {len(app.routes)}")

        # Count routes that should be affected by CORS
        cors_affected_routes = []
        for route in app.routes:
            if hasattr(route, 'path') and '/auth/' in route.path:
                cors_affected_routes.append(route.path)

        print(f"Auth routes (should have CORS): {cors_affected_routes}")

        return True
    except Exception as e:
        print(f"Error checking app state: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing middleware configuration...")
    print("="*50)

    success1 = check_middleware_config()
    success2 = check_app_state()

    print("="*50)
    if success1 and success2:
        print("Middleware configuration test completed.")
    else:
        print("Middleware configuration test failed.")