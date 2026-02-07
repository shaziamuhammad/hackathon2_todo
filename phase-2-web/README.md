# Phase 2: Secure Todo Web Application

This is a full-stack web application for managing todos with secure authentication and user isolation.

## Features

- User registration and login with JWT authentication
- Secure API endpoints with authorization checks
- User data isolation (each user only sees their own tasks)
- Full CRUD operations for tasks
- Responsive UI built with Next.js and Tailwind CSS
- Loading states, error states, and empty states

## Tech Stack

### Backend
- FastAPI (Python web framework)
- SQLModel (SQL toolkit and ORM)
- Neon Postgres (PostgreSQL database)
- JWT (JSON Web Tokens) for authentication
- Alembic (database migrations)

### Frontend
- Next.js 14 (React framework)
- TypeScript (type safety)
- Tailwind CSS (styling)
- Zustand (state management)
- Axios (HTTP client)

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login an existing user

### Task Management
- `GET /api/v1/tasks/{user_id}/tasks` - Get all tasks for a specific user
- `POST /api/v1/tasks/{user_id}/tasks` - Create a new task for a specific user
- `GET /api/v1/tasks/{user_id}/tasks/{id}` - Get a specific task for a user
- `PUT /api/v1/tasks/{user_id}/tasks/{id}` - Update a specific task for a user
- `DELETE /api/v1/tasks/{user_id}/tasks/{id}` - Delete a specific task for a user
- `PATCH /api/v1/tasks/{user_id}/tasks/{id}/complete` - Mark task as complete/incomplete

## Security Features

- JWT-based authentication with BETTER_AUTH_SECRET
- Authorization checks ensuring users can only access their own data
- All API endpoints require valid authentication token
- 401 Unauthorized for invalid/missing tokens
- 403 Forbidden when accessing another user's resources

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd phase-2-web/backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (copy `.env.example` to `.env` and update values):
```bash
cp .env.example .env
```

5. Run the development server:
```bash
uvicorn app.main:app --reload
```

The backend will be available at http://localhost:8000

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd phase-2-web/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables (copy `.env.local.example` to `.env.local` and update values):
```bash
cp .env.local.example .env.local
```

4. Run the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:3000

## Environment Variables

### Backend
- `DATABASE_URL` - Database connection string
- `BETTER_AUTH_SECRET` - Secret key for JWT signing
- `ACCESS_TOKEN_EXPIRE_MINUTES` - JWT token expiration time

### Frontend
- `NEXT_PUBLIC_API_URL` - Backend API URL (defaults to http://localhost:8000/api/v1)

## Deployment

### Frontend (to Vercel)
1. Connect your GitHub repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push to main branch

### Backend
Deploy to cloud platforms like AWS, Heroku, or Railway with environment variables configured.

## Development

### Running Tests
Backend tests:
```bash
pytest
```

Frontend tests:
```bash
npm run test
```

### Database Migrations
Backend uses Alembic for migrations:
```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```