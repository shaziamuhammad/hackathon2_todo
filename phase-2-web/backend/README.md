# Secure Todo Backend

This is the backend for the secure todo application built with FastAPI and SQLAlchemy.

## Features

- JWT-based authentication
- User data isolation
- Full CRUD operations for tasks
- Input validation
- Security measures (401/403 responses)

## API Endpoints

The backend provides the following endpoints:

- `GET /api/{user_id}/tasks` - Get all tasks for a specific user
- `POST /api/{user_id}/tasks` - Create a new task for a specific user
- `GET /api/{user_id}/tasks/{id}` - Get a specific task for a user
- `PUT /api/{user_id}/tasks/{id}` - Update a specific task for a user
- `DELETE /api/{user_id}/tasks/{id}` - Delete a specific task for a user
- `PATCH /api/{user_id}/tasks/{id}/complete` - Mark a task as complete/incomplete

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

3. Run the application:
```bash
python -m uvicorn app.main:app --reload
```

The API will run on `http://localhost:8000`.

## Environment Variables

- `BETTER_AUTH_SECRET`: Secret key for JWT token encryption (at least 32 characters)
- `DATABASE_URL`: Database connection string (defaults to SQLite)
- `ALLOWED_ORIGINS`: List of origins allowed to access the API

## Running with Docker

Build and run the container:

```bash
docker build -t secure-todo-backend .
docker run -p 8000:8000 secure-todo-backend
```