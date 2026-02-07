#!/usr/bin/env python3
"""
Debug script to test CORS configuration and API endpoints
"""
import requests
import json

# Test the backend server
BACKEND_URL = "http://localhost:8000"

def test_cors_preflight():
    """Test CORS preflight request"""
    print("Testing CORS preflight request...")
    
    headers = {
        'Origin': 'http://localhost:3000',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'Content-Type',
    }
    
    try:
        response = requests.options(f"{BACKEND_URL}/api/v1/auth/register", headers=headers)
        print(f"OPTIONS /api/v1/auth/register status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✓ Preflight request successful")
        else:
            print(f"✗ Preflight request failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Preflight request failed with error: {e}")

def test_register_endpoint():
    """Test the register endpoint"""
    print("\nTesting register endpoint...")
    
    headers = {
        'Content-Type': 'application/json',
        'Origin': 'http://localhost:3000'
    }
    
    data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/v1/auth/register",
                                headers=headers,
                                data=json.dumps(data))
        print(f"POST /api/v1/auth/register status: {response.status_code}")
        print(f"Response: {response.text[:200]}...\n")  # First 200 chars
        
        if response.status_code in [200, 201, 409]:  # 409 is expected if user exists
            print("✓ Register request successful")
        else:
            print(f"✗ Register request failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Register request failed with error: {e}")

def test_login_endpoint():
    """Test the login endpoint"""
    print("\nTesting login endpoint...")
    
    headers = {
        'Content-Type': 'application/json',
        'Origin': 'http://localhost:3000'
    }
    
    data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/v1/auth/login",
                                headers=headers,
                                data=json.dumps(data))
        print(f"POST /api/v1/auth/login status: {response.status_code}")
        print(f"Response: {response.text[:200]}...\n")  # First 200 chars
        
        if response.status_code in [200, 401]:  # 401 is expected if user doesn't exist
            print("✓ Login request successful")
        else:
            print(f"✗ Login request failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Login request failed with error: {e}")

if __name__ == "__main__":
    print("Starting CORS and API endpoint debugging...")
    print(f"Testing backend at: {BACKEND_URL}")
    
    # Check if server is running first
    try:
        health_check = requests.get(BACKEND_URL)
        print(f"✓ Server is reachable: {health_check.status_code}")
        print(f"Response: {health_check.json()}\n")
    except Exception as e:
        print(f"✗ Server is not reachable: {e}")
        print("Make sure your FastAPI server is running on http://localhost:8000")
        exit(1)
    
    test_cors_preflight()
    test_register_endpoint()
    test_login_endpoint()
    
    print("\nDebugging complete!")
