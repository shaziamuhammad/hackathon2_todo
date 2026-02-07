# Phase 2 Web Todo Application Implementation Plan

## Technical Context

### Project Overview
This plan details the implementation of a secure web-based todo application featuring Next.js 16+ frontend with FastAPI backend, JWT authentication, and secure API endpoints.

### Architecture
- **Frontend**: Next.js 16+ with App Router, TypeScript, Tailwind CSS
- **Backend**: FastAPI with SQLModel and Neon Postgres
- **Authentication**: JWT-based using BETTER_AUTH_SECRET
- **Security**: Role-based access control with user data isolation

### Current State
- Feature specification complete (specs/phase2-web/spec.md)
- No existing implementation code
- Clean project state

### Dependencies
- Node.js (v18+) for frontend
- Python (v3.9+) for backend
- Neon Postgres database
- Better Auth for authentication
- Alembic for database migrations

### Constraints
- All API endpoints must require Authorization: Bearer <token>
- Users can only access their own tasks
- Must implement exact API endpoints as specified
- Title validation (required) must be enforced

### Integration Points
- Frontend API calls to backend endpoints
- JWT token verification between frontend and backend
- Database migrations through Alembic
- Authentication flow with Better Auth

### Known Unknowns
- Specific JWT token lifetime configuration
- Neon Postgres connection pooling settings
- Better Auth integration specifics
- Vercel deployment configuration details

## Constitution Check

### Code Quality Standards
- [ ] All code follows established patterns from the constitution
- [ ] Type safety implemented with TypeScript and Python type hints
- [ ] Consistent naming conventions applied throughout

### Security Requirements
- [ ] Authentication required for all endpoints
- [ ] Authorization checks verify user owns accessed resources
- [ ] JWT tokens validated using BETTER_AUTH_SECRET
- [ ] SQL injection prevention through SQLModel/ORM
- [ ] Input validation for all user-provided data

### Performance Requirements
- [ ] Database queries optimized with proper indexing
- [ ] Efficient API responses without over-fetching
- [ ] Minimal bundle sizes for frontend assets

### Architecture Patterns
- [ ] Separation of concerns between frontend and backend
- [ ] Proper API design following REST conventions
- [ ] Database models match specification requirements

### Testing Requirements
- [ ] Unit tests for core business logic
- [ ] Integration tests for API endpoints
- [ ] Authentication flow tests
- [ ] Security tests for access control

## Research Phase

### Resolved Unknowns

**Decision**: JWT Token Configuration
**Rationale**: Standard JWT tokens should have a 15-30 minute expiration for security
**Alternatives considered**: Longer sessions (convenience), shorter sessions (security)

**Decision**: Neon Postgres Connection Pooling
**Rationale**: Use SQLModel's built-in connection pooling with reasonable defaults
**Alternatives considered**: Custom connection pool, single connection

**Decision**: Better Auth Integration
**Rationale**: Since Better Auth manages JWTs, we'll create our own token verification system alongside it
**Alternatives considered**: Replace Better Auth with custom solution, integrate only with Better Auth

**Decision**: Vercel Deployment Configuration
**Rationale**: Use standard Next.js deployment configuration with environment variables
**Alternatives considered**: Alternative hosting platforms

## Phase 1: Design & Contracts

### Data Model

#### User Entity
- id (Integer, Primary Key, Auto-increment)
- email (String, Unique, Not Null)
- hashed_password (String, Not Null)
- created_at (DateTime, Default now)
- updated_at (DateTime, Default now, On Update)

#### Task Entity
- id (Integer, Primary Key, Auto-increment)
- title (String, Not Null)
- description (String, Optional)
- completed (Boolean, Default False)
- user_id (Integer, Foreign Key to User, Not Null)
- created_at (DateTime, Default now)
- updated_at (DateTime, Default now, On Update)

### API Contracts

#### Authentication Endpoints
```
POST /api/auth/login
- Request: {email: string, password: string}
- Response: {access_token: string, token_type: "bearer"}
- Error: 401 Unauthorized

POST /api/auth/register
- Request: {email: string, password: string}
- Response: {access_token: string, token_type: "bearer"}
- Error: 400 Bad Request, 409 Conflict
```

#### Task Management Endpoints
```
GET /api/{user_id}/tasks
- Headers: Authorization: Bearer {token}
- Response: Task[]
- Error: 401 Unauthorized, 403 Forbidden, 404 Not Found

POST /api/{user_id}/tasks
- Headers: Authorization: Bearer {token}
- Request: {title: string, description?: string}
- Response: Task
- Error: 401 Unauthorized, 403 Forbidden, 422 Validation Error

GET /api/{user_id}/tasks/{id}
- Headers: Authorization: Bearer {token}
- Response: Task
- Error: 401 Unauthorized, 403 Forbidden, 404 Not Found

PUT /api/{user_id}/tasks/{id}
- Headers: Authorization: Bearer {token}
- Request: {title: string, description?: string, completed?: boolean}
- Response: Task
- Error: 401 Unauthorized, 403 Forbidden, 404 Not Found, 422 Validation Error

DELETE /api/{user_id}/tasks/{id}
- Headers: Authorization: Bearer {token}
- Response: {message: string}
- Error: 401 Unauthorized, 403 Forbidden, 404 Not Found

PATCH /api/{user_id}/tasks/{id}/complete
- Headers: Authorization: Bearer {token}
- Request: {completed: boolean}
- Response: Task
- Error: 401 Unauthorized, 403 Forbidden, 404 Not Found
```

### Frontend Architecture

#### App Router Structure
```
app/
├── layout.tsx
├── page.tsx (redirects to /dashboard)
├── login/
│   └── page.tsx
├── dashboard/
│   └── page.tsx
└── globals.css
```

#### Component Structure
- TaskList component with loading/empty/error states
- TaskForm component with validation
- AuthProvider for JWT token management
- API service with automatic token attachment

## Implementation Plan

### Backend Implementation

#### Week 1: Project Setup and Authentication
1. Set up FastAPI project structure
2. Configure SQLModel with Neon Postgres
3. Implement JWT authentication with BETTER_AUTH_SECRET
4. Create User model and authentication endpoints
5. Set up Alembic for database migrations

#### Week 2: Task Management API
1. Create Task model with relationships
2. Implement required API endpoints with security checks
3. Add input validation and error handling
4. Create API documentation with Swagger/OpenAPI
5. Implement user data isolation checks

#### Week 3: Testing and Optimization
1. Write unit tests for all endpoints
2. Perform security testing for authorization
3. Optimize database queries
4. Set up environment configuration

### Frontend Implementation

#### Week 4: Project Setup and UI Framework
1. Set up Next.js 16+ with App Router
2. Configure TypeScript and Tailwind CSS
3. Implement responsive layout and design system
4. Set up API service with JWT handling

#### Week 5: Authentication Flow
1. Create login and registration pages
2. Implement AuthProvider with token management
3. Create protected routes
4. Add loading, error, and empty state components

#### Week 6: Task Management Interface
1. Build dashboard with task list
2. Create task creation and editing forms
3. Implement real-time updates
4. Add task completion toggle functionality

### Local Development Setup

#### Prerequisites
- Node.js v18+
- Python v3.9+
- Neon Postgres account

#### Backend Setup
```bash
cd phase-2-web/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Update .env with your database URL and JWT secret
alembic upgrade head
uvicorn main:app --reload
```

#### Frontend Setup
```bash
cd phase-2-web/frontend
npm install
cp .env.example .env.local
# Update .env.local with your backend URL
npm run dev
```

### Deployment Strategy

#### Backend Deployment
- Deploy to cloud platform (Heroku, AWS, or Railway)
- Configure environment variables
- Set up automated deployments from main branch
- Configure database connection for production

#### Frontend Deployment
- Deploy to Vercel
- Connect to Git repository
- Configure build settings and environment variables
- Set up automated deployments from main branch

### Security Implementation

#### JWT Token Verification
- Backend verifies all tokens using BETTER_AUTH_SECRET
- User ID extracted from token compared with URL parameter
- 401 returned for invalid/missing tokens
- 403 returned when token user_id != URL user_id

#### Data Isolation
- All queries filtered by user_id from token
- Foreign key relationships enforce integrity
- Additional server-side checks prevent cross-user access

#### Input Validation
- Title required validation on all create/update operations
- Description optional but sanitized if provided
- All inputs validated before database operations

### Testing Strategy

#### Backend Tests
- Unit tests for API endpoints
- Integration tests for authentication flow
- Security tests for authorization
- Database transaction tests

#### Frontend Tests
- Component rendering tests
- User interaction tests
- API integration tests
- Authentication flow tests

## Success Criteria

### Functional Requirements
- [ ] All 6 required API endpoints implemented and secured
- [ ] JWT authentication working with BETTER_AUTH_SECRET
- [ ] User data isolation enforced
- [ ] Input validation working (title required)
- [ ] Responsive dashboard UI implemented

### Performance Requirements
- [ ] API response time < 1 second for simple operations
- [ ] Dashboard loads in under 3 seconds
- [ ] Authentication flow completes in under 5 seconds

### Security Requirements
- [ ] All endpoints require valid JWT token
- [ ] 401 returned for invalid/missing tokens
- [ ] 403 returned when accessing other users' data
- [ ] No sensitive data exposed in client

### Quality Requirements
- [ ] All code follows established patterns
- [ ] Proper error handling implemented
- [ ] Loading and error states handled
- [ ] Responsive design works on mobile/tablet/desktop