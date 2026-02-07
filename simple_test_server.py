from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

# Create a simple app with CORS
app = FastAPI(title="Test API")

# Add CORS middleware with the same configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Test server running"}

# Create a simple auth router
auth_router = APIRouter()

@auth_router.post("/register")
def register_test():
    return {"message": "registered"}

@auth_router.post("/login")
def login_test():
    return {"message": "logged in"}

# Include the router
app.include_router(auth_router, prefix="/auth", tags=["auth"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)