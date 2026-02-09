# Data Model: AI-Powered Todo Chatbot

**Feature**: AI-Powered Todo Chatbot
**Date**: 2026-02-08

## Entities

### TodoItem
- **id**: string (UUID) - Unique identifier for the task
- **title**: string (required, max 255 chars) - Task title
- **description**: string (optional, max 1000 chars) - Task description
- **priority**: enum ['low', 'medium', 'high', 'urgent'] (default: 'medium') - Task priority level
- **tags**: array of strings - Tags for categorization
- **status**: enum ['pending', 'in-progress', 'complete'] (default: 'pending') - Task completion status
- **due_date**: datetime (optional) - Due date and time for the task
- **created_at**: datetime - Timestamp when task was created
- **updated_at**: datetime - Timestamp when task was last updated
- **completed_at**: datetime (optional) - Timestamp when task was completed
- **recurrence_pattern**: object (optional) - Recurrence pattern for recurring tasks
  - type: enum ['daily', 'weekly', 'monthly', 'yearly']
  - interval: integer
  - days_of_week: array of integers (for weekly)
  - day_of_month: integer (for monthly)
  - ends_on: datetime (optional)
- **user_id**: string (foreign key) - Reference to the user who owns the task

### User
- **id**: string (UUID) - Unique identifier for the user
- **email**: string (required, unique) - User's email address
- **name**: string (required) - User's full name
- **password_hash**: string (optional) - Hashed password for email authentication
- **provider**: enum ['google', 'facebook', 'email'] (required) - Authentication provider
- **provider_id**: string (optional) - Provider-specific user ID
- **theme_preference**: enum ['light', 'dark', 'purple'] (default: 'light') - Preferred UI theme
- **created_at**: datetime - Timestamp when user was created
- **updated_at**: datetime - Timestamp when user was last updated

### UserSession
- **id**: string (UUID) - Unique identifier for the session
- **user_id**: string (foreign key) - Reference to the associated user
- **token**: string (encrypted) - Session token
- **expires_at**: datetime - Expiration timestamp
- **created_at**: datetime - Timestamp when session was created

### Conversation
- **id**: string (UUID) - Unique identifier for the conversation
- **user_id**: string (foreign key) - Reference to the user
- **messages**: array of objects - Chat messages in the conversation
  - role: enum ['user', 'assistant']
  - content: string
  - timestamp: datetime
- **created_at**: datetime - Timestamp when conversation started
- **updated_at**: datetime - Timestamp when conversation was last updated

## Relationships
- User 1:* TodoItem (one user can have many todo items)
- User 1:* UserSession (one user can have many sessions)
- User 1:* Conversation (one user can have many conversations)

## Validation Rules
- TodoItem.title is required and must be 1-255 characters
- TodoItem.due_date must be in the future if provided
- TodoItem.priority must be one of the allowed values
- User.email must be valid email format and unique
- User.name is required
- Recurrence pattern is required for recurring tasks

## State Transitions
- TodoItem.status: pending → in-progress → complete (unidirectional)
- UserSession.expires_at: session becomes invalid after this time