# Quickstart Guide: AI-Powered Todo Chatbot

**Feature**: AI-Powered Todo Chatbot
**Date**: 2026-02-08

## Prerequisites

- Python 3.13+ installed
- Node.js 18+ installed
- NeonDB account and connection string
- Anthropic API key (or OpenAI API key as fallback)

## Environment Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Install backend dependencies:
```bash
cd backend
pip install fastapi uvicorn python-multipart pydantic fastmcp anthropic openai python-jose[cryptography] passlib[bcrypt] sqlalchemy psycopg2-binary python-dateutil
```

3. Install frontend dependencies:
```bash
cd ../frontend
npm install
```

## Configuration

1. Create `.env` file in the backend directory:
```env
DATABASE_URL=<your-neon-db-url>
ANTHROPIC_API_KEY=<your-anthropic-api-key>
OPENAI_API_KEY=<your-openai-api-key>
SECRET_KEY=<your-secret-key-for-jwt>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
MCP_SERVER_URL=http://localhost:8001
```

## Running the Application

1. Start the MCP server:
```bash
cd backend
python mcp_server.py
```

2. In a new terminal, start the main backend:
```bash
cd backend
uvicorn main:app --reload --port 8000
```

3. In another terminal, start the frontend:
```bash
cd frontend
npm run dev
```

## MCP Server Setup

The MCP server exposes the following tools for the AI agent:
- `add_task`: Create a new todo item
- `delete_task`: Remove a todo item
- `update_task`: Update an existing todo item
- `list_tasks`: Retrieve user's todo items
- `mark_complete`: Mark a task as completed
- `search_tasks`: Search tasks by criteria
- `set_due_date`: Set due date for a task
- `set_priority`: Set priority level for a task

## Natural Language Commands

The AI agent supports the following command patterns:
- "Add a task to [task description]"
- "Create a [priority level] task to [task description]"
- "Delete the [task name] task"
- "Update the [task name] task to [new details]"
- "Mark [task name] as complete"
- "Show me all [priority level] tasks"
- "Set a due date for [task name] on [date]"
- "Create a recurring task that [description] every [frequency]"

## API Endpoints

- `POST /api/chat`: Process natural language commands
- `GET /api/tasks`: List all user tasks
- `POST /api/tasks`: Create a new task
- `PUT /api/tasks/{id}`: Update a task
- `DELETE /api/tasks/{id}`: Delete a task
- `POST /api/auth/login`: User authentication
- `POST /api/auth/register`: User registration

## Development

To extend functionality:
1. Add new MCP tools in `mcp_server.py`
2. Update the AI agent's tool usage in `ai_agent.py`
3. Extend the frontend components in `ChatWidget.tsx`
4. Update the API contracts in `contracts/api.yaml`