import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'phase-2-web', 'backend'))

# Change to the backend directory
os.chdir(os.path.join(os.getcwd(), 'phase-2-web', 'backend'))

print("Starting FastAPI server with corrected CORS configuration...")
print("Current directory:", os.getcwd())

try:
    from app.main import app
    import uvicorn
    print("Successfully imported app and uvicorn")
    print("Starting server on http://0.0.0.0:8000...")

    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)

except ImportError as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"Error starting server: {e}")
    import traceback
    traceback.print_exc()