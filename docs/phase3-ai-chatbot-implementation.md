# Phase 3: AI-Powered Todo Chatbot Implementation

## Overview

Phase 3 adds AI-powered natural language processing to the Todo application, allowing users to manage tasks through conversational chat. The implementation uses OpenAI Assistants API with Model Context Protocol (MCP) for tool integration.

---

## Architecture

### Components

1. **MCP Server** (`app/mcp_server.py`)
   - Exposes Todo CRUD operations as MCP tools
   - Handles database interactions
   - Returns structured responses

2. **AI Agent** (`app/ai_agent/agent.py`)
   - OpenAI Assistants API integration
   - Manages conversation threads
   - Handles tool calling and execution

3. **Chat Endpoint** (`app/api/v1/endpoints/chat.py`)
   - REST API endpoint for chat interactions
   - Manages conversation state
   - Authenticates users

4. **Frontend Integration**
   - ChatWidget component (already implemented)
   - Notification service for task reminders
   - Notification settings component

---

## Features Implemented

### ✅ Group 1: Dependencies

**Added to requirements.txt:**
- `fastmcp>=0.1.0` - MCP server framework
- `anthropic>=0.18.0` - Anthropic AI (backup)
- `openai>=1.12.0` - OpenAI Assistants API
- `psycopg2-binary>=2.9.9` - Database migrations

### ✅ Group 2: MCP Server

**File:** `phase-2-web/backend/app/mcp_server.py`

**Exposed Tools:**
1. **add_task** - Create new tasks with:
   - Title (required)
   - Description, priority, due date, tags
   - Recurrence patterns (e.g., weekly, monthly)

2. **list_tasks** - List and filter tasks by:
   - Completion status
   - Priority (low, medium, high, urgent)
   - Status (pending, in-progress, complete)
   - Tags
   - Sort by: created_at, due_date, priority, title
   - Sort order: asc, desc

3. **update_task** - Update existing tasks:
   - All fields modifiable
   - Validates task ownership

4. **delete_task** - Delete tasks:
   - Validates task ownership
   - Returns confirmation

5. **mark_complete** - Toggle completion status:
   - Updates completed flag
   - Sets completion timestamp
   - Updates status field

### ✅ Group 3: AI Agent Configuration

**File:** `phase-2-web/backend/app/ai_agent/agent.py`

**Features:**
- OpenAI Assistants API integration
- Conversation thread management
- Tool calling with MCP integration
- Natural language understanding for:
  - Task creation with complex details
  - Filtering and searching tasks
  - Updating multiple fields
  - Parsing dates and priorities
  - Understanding recurrence patterns

**Assistant Instructions:**
- Conversational and helpful tone
- Proactive clarification
- Confirmation before destructive actions
- Clear result presentation

### ✅ Group 4: Chat Endpoint

**File:** `phase-2-web/backend/app/api/v1/endpoints/chat.py`

**Endpoints:**
- `POST /api/v1/chat` - Send message to AI assistant
- `DELETE /api/v1/chat/{conversation_id}` - Delete conversation

**Features:**
- JWT authentication
- Conversation thread persistence
- Message validation (max 2000 chars)
- Error handling and logging
- User isolation (users can only access their conversations)

### ✅ Group 5: Frontend Integration

**Already Implemented:**
- ChatWidget component (`components/ChatWidget.tsx`)
- API integration with `/api/v1/chat`
- Message history display
- Loading states and error handling

### ✅ Group 6: Advanced Parsing

**Implemented through AI Agent:**

1. **Recurring Tasks:**
   - Patterns: weekly, monthly, daily, yearly
   - Custom intervals (e.g., "every 2 weeks")
   - Stored as JSON: `{"frequency": "weekly", "interval": 1}`

2. **Due Dates:**
   - Natural language parsing: "tomorrow", "next Monday", "in 3 days"
   - ISO format support: YYYY-MM-DD, YYYY-MM-DDTHH:MM:SS
   - Timezone handling

3. **Priorities:**
   - Levels: low, medium, high, urgent
   - Natural language: "important task", "urgent meeting"

4. **Search, Filter, Sort:**
   - Filter by: completion, priority, status, tags
   - Sort by: created_at, due_date, priority, title
   - Sort order: ascending, descending

**Example Queries:**
```
"Add buy groceries with high priority due tomorrow"
"Show me all urgent tasks"
"List incomplete tasks sorted by due date"
"Mark the meeting task as complete"
"Update project proposal to high priority"
```

### ✅ Group 7: UI Enhancements

**Already Completed (Previous Work):**
- Responsive design (mobile, tablet, desktop)
- Header with hamburger menu
- Footer with responsive grid
- Sidebar with collapsible navigation
- Purple theme with light/dark mode toggle
- Touch-friendly interactions

### ✅ Group 8: Browser Notifications

**Files Created:**
1. `services/notificationService.ts` - Core notification service
2. `components/NotificationSettings.tsx` - Settings UI
3. `hooks/useTaskNotifications.ts` - React hook for notifications

**Features:**
- Permission request handling
- Task due date notifications:
  - Overdue tasks (immediate)
  - Due within 1 hour
  - Due within 24 hours (once per day)
- Task completion notifications
- Task creation notifications
- Periodic checking (every 15 minutes)
- Browser compatibility detection
- Permission status display

---

## Environment Variables

**Required in `.env`:**

```bash
# AI Services (at least one required)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...  # Optional backup

# MCP Server (optional, defaults to localhost:8001)
MCP_SERVER_URL=http://localhost:8001

# Database
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dbname

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

---

## Installation & Setup

### 1. Install Dependencies

```bash
cd phase-2-web/backend
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 3. Run Database Migrations

```bash
alembic upgrade head
```

### 4. Start Backend Server

```bash
uvicorn app.main:app --reload --port 8000
```

### 5. Start Frontend

```bash
cd ../frontend
npm install
npm run dev
```

---

## Usage Examples

### Creating Tasks

**User:** "Add buy groceries with high priority due tomorrow"

**AI Response:** "I've created a new task 'Buy groceries' with high priority, due tomorrow at [date]. Would you like to add any tags or description?"

### Listing Tasks

**User:** "Show me all my urgent tasks"

**AI Response:** "Here are your urgent tasks:
1. Project deadline - Due in 2 hours
2. Client meeting - Due tomorrow
3. Report submission - Overdue by 1 day"

### Updating Tasks

**User:** "Change the project deadline to next Monday"

**AI Response:** "I've updated the 'Project deadline' task. The new due date is Monday, [date]."

### Recurring Tasks

**User:** "Create a weekly task to review emails every Monday"

**AI Response:** "I've created a recurring task 'Review emails' that repeats every Monday. You'll see a new instance each week."

---

## API Documentation

### Chat Endpoint

**POST /api/v1/chat**

Request:
```json
{
  "message": "Add buy groceries with high priority",
  "conversation_id": "optional-thread-id"
}
```

Response:
```json
{
  "response": "I've created a new task 'Buy groceries' with high priority.",
  "conversation_id": "thread_abc123"
}
```

**DELETE /api/v1/chat/{conversation_id}**

Response:
```json
{
  "message": "Conversation deleted successfully"
}
```

---

## MCP Tools Reference

### add_task

```python
{
  "user_id": "uuid",
  "title": "Task title",
  "description": "Optional description",
  "priority": "low|medium|high|urgent",
  "due_date": "2024-12-31T23:59:59",
  "tags": ["tag1", "tag2"],
  "recurrence_pattern": {
    "frequency": "weekly",
    "interval": 1
  }
}
```

### list_tasks

```python
{
  "user_id": "uuid",
  "completed": true|false|null,
  "priority": "low|medium|high|urgent",
  "status": "pending|in-progress|complete",
  "tag": "tag_name",
  "sort_by": "created_at|due_date|priority|title",
  "sort_order": "asc|desc"
}
```

### update_task

```python
{
  "user_id": "uuid",
  "task_id": "uuid",
  "title": "New title",
  "description": "New description",
  "priority": "high",
  "status": "in-progress",
  "tags": ["updated", "tags"],
  "due_date": "2024-12-31",
  "recurrence_pattern": {...}
}
```

### delete_task

```python
{
  "user_id": "uuid",
  "task_id": "uuid"
}
```

### mark_complete

```python
{
  "user_id": "uuid",
  "task_id": "uuid",
  "completed": true|false
}
```

---

## Testing

### Manual Testing Checklist

**Chat Functionality:**
- [ ] Send simple message: "Add task to buy milk"
- [ ] Create task with priority: "Add urgent task to call client"
- [ ] Create task with due date: "Add task due tomorrow"
- [ ] List all tasks: "Show me all my tasks"
- [ ] Filter tasks: "Show me high priority tasks"
- [ ] Update task: "Change buy milk to high priority"
- [ ] Mark complete: "Mark the call client task as done"
- [ ] Delete task: "Delete the buy milk task"

**Notifications:**
- [ ] Enable notifications in settings
- [ ] Create task due in 1 hour
- [ ] Verify notification appears
- [ ] Complete task and verify completion notification
- [ ] Check overdue task notification

**Conversation Continuity:**
- [ ] Start conversation
- [ ] Send multiple messages
- [ ] Verify context is maintained
- [ ] Refresh page and continue conversation

---

## Troubleshooting

### Issue: "OPENAI_API_KEY not found"
**Solution:** Add your OpenAI API key to `.env` file

### Issue: "MCP tools not working"
**Solution:** Verify database connection and user authentication

### Issue: "Notifications not showing"
**Solution:**
1. Check browser permissions
2. Ensure HTTPS (required for notifications in production)
3. Verify notification service is initialized

### Issue: "Conversation not persisting"
**Solution:** Check that conversation_id is being stored and passed correctly

---

## Performance Considerations

1. **OpenAI API Calls:**
   - Each message = 1 API call
   - Tool calls = additional processing time
   - Consider caching for repeated queries

2. **Database Queries:**
   - MCP tools use async database sessions
   - Indexed on user_id and task_id
   - Efficient filtering with SQLModel

3. **Notification Checking:**
   - Runs every 15 minutes by default
   - Configurable interval
   - Uses localStorage to prevent duplicate notifications

---

## Security

1. **Authentication:**
   - All endpoints require JWT token
   - User isolation enforced
   - Conversation ownership validated

2. **Input Validation:**
   - Message length limited to 2000 chars
   - SQL injection prevented by SQLModel
   - XSS protection in frontend

3. **API Keys:**
   - Stored in environment variables
   - Never exposed to frontend
   - Rotated regularly

---

## Future Enhancements

1. **Conversation Persistence:**
   - Store conversations in database
   - Conversation history UI
   - Export conversations

2. **Advanced NLP:**
   - Multi-task operations
   - Bulk updates
   - Smart suggestions

3. **Voice Integration:**
   - Speech-to-text input
   - Text-to-speech responses

4. **Analytics:**
   - Task completion trends
   - Productivity insights
   - AI usage statistics

---

## Summary

Phase 3 successfully implements an AI-powered chatbot for todo management with:
- ✅ Natural language task creation and management
- ✅ OpenAI Assistants API integration
- ✅ MCP tool framework for CRUD operations
- ✅ Advanced parsing (priorities, due dates, recurrence)
- ✅ Browser notifications for task reminders
- ✅ Secure, authenticated API endpoints
- ✅ Responsive UI integration

All requirements from the task breakdown have been implemented and are ready for testing.
