# API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Most endpoints require authentication using JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

---

## Authentication Endpoints

### Register User

Create a new user account.

**Endpoint:** `POST /auth/register`

**Authentication:** Not required

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": null,
    "theme_preference": "light",
    "provider": "email",
    "created_at": "2026-02-08T10:00:00Z"
  }
}
```

**Error Responses:**
- `409 Conflict` - Email already registered
- `400 Bad Request` - Invalid password (too short or too long)

---

### Login

Authenticate with email and password.

**Endpoint:** `POST /auth/login`

**Authentication:** Not required

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "theme_preference": "dark"
  }
}
```

**Error Responses:**
- `401 Unauthorized` - Incorrect email or password

---

### OAuth Authentication

Authenticate using OAuth provider (Google, Facebook).

**Endpoint:** `POST /auth/oauth`

**Authentication:** Not required

**Request Body:**
```json
{
  "provider": "google",
  "access_token": "ya29.a0AfH6SMBx...",
  "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6...",
  "email": "user@example.com",
  "name": "John Doe"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "John Doe"
}
```

**Supported Providers:**
- `google` - Google OAuth
- `facebook` - Facebook OAuth

**Error Responses:**
- `400 Bad Request` - Unsupported OAuth provider
- `401 Unauthorized` - Invalid OAuth token
- `500 Internal Server Error` - OAuth verification failed

---

## Task Management Endpoints

### List Tasks

Retrieve all tasks for the authenticated user with optional filtering and sorting.

**Endpoint:** `GET /tasks`

**Authentication:** Required

**Query Parameters:**
- `priority` (optional) - Filter by priority: `low`, `medium`, `high`, `urgent`
- `status` (optional) - Filter by status: `pending`, `in-progress`, `complete`
- `tag` (optional) - Filter by tag
- `sort_by` (optional) - Sort field: `created_at`, `due_date`, `priority` (default: `created_at`)
- `order` (optional) - Sort order: `asc`, `desc` (default: `desc`)
- `limit` (optional) - Maximum results (default: 100)

**Example Request:**
```
GET /tasks?priority=high&status=pending&sort_by=due_date&order=asc
```

**Response:** `200 OK`
```json
{
  "tasks": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Finish project report",
      "description": "Complete the Q1 project report",
      "priority": "high",
      "status": "pending",
      "tags": ["work", "urgent"],
      "due_date": "2026-02-15T17:00:00Z",
      "recurrence_pattern": null,
      "created_at": "2026-02-08T10:00:00Z",
      "updated_at": "2026-02-08T10:00:00Z",
      "completed_at": null
    }
  ],
  "count": 1
}
```

---

### Create Task

Create a new task.

**Endpoint:** `POST /tasks`

**Authentication:** Required

**Request Body:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "medium",
  "status": "pending",
  "tags": ["personal", "shopping"],
  "due_date": "2026-02-09T18:00:00Z",
  "recurrence_pattern": {
    "type": "weekly",
    "interval": 1,
    "day_of_week": 6
  }
}
```

**Field Descriptions:**
- `title` (required) - Task title
- `description` (optional) - Task description
- `priority` (optional) - Priority level (default: `medium`)
- `status` (optional) - Task status (default: `pending`)
- `tags` (optional) - Array of tags
- `due_date` (optional) - Due date in ISO 8601 format
- `recurrence_pattern` (optional) - Recurrence configuration

**Recurrence Pattern Schema:**
```json
{
  "type": "daily|weekly|monthly|yearly",
  "interval": 1,
  "day_of_week": 0-6,  // For weekly (0=Sunday, 6=Saturday)
  "day_of_month": 1-31  // For monthly
}
```

**Response:** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "medium",
  "status": "pending",
  "tags": ["personal", "shopping"],
  "due_date": "2026-02-09T18:00:00Z",
  "recurrence_pattern": {
    "type": "weekly",
    "interval": 1,
    "day_of_week": 6
  },
  "created_at": "2026-02-08T10:00:00Z",
  "updated_at": "2026-02-08T10:00:00Z",
  "completed_at": null
}
```

**Error Responses:**
- `422 Unprocessable Entity` - Invalid request data

---

### Get Task

Retrieve a specific task by ID.

**Endpoint:** `GET /tasks/{task_id}`

**Authentication:** Required

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "medium",
  "status": "pending",
  "tags": ["personal", "shopping"],
  "due_date": "2026-02-09T18:00:00Z",
  "recurrence_pattern": null,
  "created_at": "2026-02-08T10:00:00Z",
  "updated_at": "2026-02-08T10:00:00Z",
  "completed_at": null
}
```

**Error Responses:**
- `404 Not Found` - Task not found or not owned by user

---

### Update Task

Update an existing task.

**Endpoint:** `PUT /tasks/{task_id}`

**Authentication:** Required

**Request Body:** (all fields optional)
```json
{
  "title": "Buy groceries and supplies",
  "description": "Milk, eggs, bread, cleaning supplies",
  "priority": "high",
  "status": "in-progress",
  "tags": ["personal", "shopping", "urgent"],
  "due_date": "2026-02-09T16:00:00Z"
}
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries and supplies",
  "description": "Milk, eggs, bread, cleaning supplies",
  "priority": "high",
  "status": "in-progress",
  "tags": ["personal", "shopping", "urgent"],
  "due_date": "2026-02-09T16:00:00Z",
  "recurrence_pattern": null,
  "created_at": "2026-02-08T10:00:00Z",
  "updated_at": "2026-02-08T11:30:00Z",
  "completed_at": null
}
```

**Error Responses:**
- `404 Not Found` - Task not found or not owned by user
- `422 Unprocessable Entity` - Invalid request data

---

### Delete Task

Delete a task.

**Endpoint:** `DELETE /tasks/{task_id}`

**Authentication:** Required

**Response:** `204 No Content`

**Error Responses:**
- `404 Not Found` - Task not found or not owned by user

---

## AI Chat Endpoint

### Process Natural Language Command

Send a natural language command to the AI agent for processing.

**Endpoint:** `POST /chat`

**Authentication:** Required

**Request Body:**
```json
{
  "message": "Add buy groceries tomorrow with high priority",
  "conversation_id": "660e8400-e29b-41d4-a716-446655440000"
}
```

**Field Descriptions:**
- `message` (required) - Natural language command (max 2000 characters)
- `conversation_id` (optional) - Conversation ID for context

**Response:** `200 OK`
```json
{
  "response": "✓ I've added 'buy groceries' to your todo list with high priority for tomorrow.",
  "action_taken": "add_task",
  "tasks_modified": [
    {
      "title": "buy groceries",
      "priority": "high",
      "due_date": "2026-02-09T00:00:00Z",
      "user_id": "550e8400-e29b-41d4-a716-446655440000"
    }
  ],
  "conversation_id": "660e8400-e29b-41d4-a716-446655440000"
}
```

**Supported Actions:**
- `add_task` - Create new task
- `delete_task` - Delete task
- `update_task` - Update task
- `mark_complete` - Mark task as complete
- `list_tasks` - List tasks
- `search_tasks` - Search tasks

**Example Commands:**
- "Add buy groceries tomorrow"
- "Create high priority task finish report"
- "List all my tasks"
- "Mark task complete"
- "Delete the groceries task"
- "Add weekly meeting every Monday at 10am"
- "Show tasks due this week"

**Error Responses:**
- `422 Unprocessable Entity` - Empty message or message too long
- `503 Service Unavailable` - AI service temporarily unavailable
- `500 Internal Server Error` - Processing failed

---

## Notification Endpoints

### Get Pending Notifications

Retrieve all pending notifications for the authenticated user.

**Endpoint:** `GET /notifications`

**Authentication:** Required

**Response:** `200 OK`
```json
{
  "status": "success",
  "notifications": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440000",
      "task_id": "550e8400-e29b-41d4-a716-446655440000",
      "task_title": "Finish project report",
      "due_date": "2026-02-09T17:00:00Z",
      "notification_time": "2026-02-09T16:00:00Z",
      "sent": false,
      "created_at": "2026-02-08T10:00:00Z"
    }
  ],
  "count": 1
}
```

**Error Responses:**
- `500 Internal Server Error` - Failed to fetch notifications

---

### Mark Notification as Sent

Mark a notification as sent/read.

**Endpoint:** `POST /notifications/{notification_id}/mark-sent`

**Authentication:** Required

**Response:** `200 OK`
```json
{
  "status": "success",
  "message": "Notification marked as sent"
}
```

**Error Responses:**
- `404 Not Found` - Notification not found
- `500 Internal Server Error` - Failed to mark notification

---

## User Preferences Endpoint

### Update User Preferences

Update user preferences including theme.

**Endpoint:** `PUT /user/preferences`

**Authentication:** Required

**Request Body:**
```json
{
  "theme_preference": "dark"
}
```

**Valid Theme Values:**
- `light` - Light theme
- `dark` - Dark theme
- `purple` - Purple theme

**Response:** `200 OK`
```json
{
  "status": "success",
  "message": "Preferences updated successfully",
  "preferences": {
    "theme_preference": "dark"
  }
}
```

**Error Responses:**
- `422 Unprocessable Entity` - Invalid theme value
- `500 Internal Server Error` - Failed to update preferences

---

## Error Response Format

All error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common HTTP Status Codes:**
- `200 OK` - Request succeeded
- `201 Created` - Resource created successfully
- `204 No Content` - Request succeeded with no response body
- `400 Bad Request` - Invalid request format
- `401 Unauthorized` - Authentication required or failed
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource already exists
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Service temporarily unavailable

---

## Rate Limiting

API endpoints are rate-limited to prevent abuse:

- **Chat endpoint:** 20 requests per minute per user
- **Other endpoints:** 100 requests per minute per user

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 20
X-RateLimit-Remaining: 15
X-RateLimit-Reset: 1644336000
```

---

## Pagination

List endpoints support pagination using query parameters:

- `limit` - Number of results per page (default: 100, max: 1000)
- `offset` - Number of results to skip (default: 0)

Example:
```
GET /tasks?limit=50&offset=100
```

---

## Webhooks (Future Feature)

Webhook support for real-time notifications is planned for a future release.

---

## API Versioning

The API uses URL versioning. The current version is `v1`:

```
/api/v1/...
```

Breaking changes will be introduced in new versions (v2, v3, etc.) while maintaining backward compatibility for older versions.

---

## Interactive API Documentation

FastAPI provides interactive API documentation:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

These interfaces allow you to:
- Browse all endpoints
- View request/response schemas
- Test endpoints directly in the browser
- Download OpenAPI specification

---

## SDK and Client Libraries

Official client libraries are planned for:
- Python
- JavaScript/TypeScript
- Go

Community contributions for other languages are welcome.

---

## Support

For API support:
- Check the interactive documentation at `/docs`
- Review the README.md for setup instructions
- Report issues on GitHub

---

## Changelog

### Version 1.0.0 (Phase 3)
- Added AI chat endpoint with natural language processing
- Added OAuth authentication support
- Added notification endpoints
- Added user preferences endpoint
- Enhanced task model with recurrence patterns
- Added comprehensive logging and error handling

### Version 0.2.0 (Phase 2)
- Initial REST API implementation
- Task CRUD operations
- Email/password authentication
- JWT token-based auth

### Version 0.1.0 (Phase 1)
- Console-based application
- Basic task management
