import requests
import sys

def test_server_endpoints():
    print("Testing server endpoints...")
    
    # Test the health of the server
    try:
        response = requests.get("http://localhost:8000/")
        print(f"Root endpoint: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Server not running: {e}")
        print("Please start your FastAPI server with: uvicorn app.main:app --reload")
        sys.exit(1)
    
    # Test the health endpoint
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Health endpoint: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Health endpoint error: {e}")
    
    # Test the problematic auth endpoints
    print("\Testing auth endpoints...")
    
    # Test OPTIONS (preflight) - this is what's failing
    try:
        options_resp = requests.options(
            "http://localhost:8000/api/v1/auth/register",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type",
            }
        )
        print(f"OPTIONS /api/v1/auth/register: {options_resp.status_code}")
        print(f"CORS headers: {[h for h in options_resp.headers.keys() if 'access-control' in h.lower()]}")
    except Exception as e:
        print(f"OPTIONS request failed: {e}")
    
    # Test GET to see if route exists
    try:
        get_resp = requests.get("http://localhost:8000/api/v1/auth/register")
        print(f"GET /api/v1/auth/register: {get_resp.status_code}")
    except Exception as e:
        print(f"GET request failed: {e}")

if __name__ == "__main__":
    test_server_endpoints()
