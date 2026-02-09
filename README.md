# AI-Powered Todo Application

A full-stack todo management application with AI-powered natural language processing, built with FastAPI, Next.js, and Claude/GPT integration.

## Overview

This project implements a comprehensive todo management system across three phases:

- **Phase 1**: Console-based todo application
- **Phase 2**: Web application with REST API and React frontend
- **Phase 3**: AI-powered chatbot with natural language processing, recurring tasks, notifications, and enhanced UI

## Features

### User Story 1: Natural Language Todo Management (MVP)
- Natural language command processing ("Add buy groceries tomorrow")
- AI-powered intent analysis using Anthropic Claude or OpenAI GPT
- MCP (Model Context Protocol) server for standardized tool access
- Conversation history and context management
- Real-time chat interface

### User Story 2: Advanced Todo Features
- Recurring tasks (daily, weekly, monthly, custom patterns)
- Natural language date parsing ("tomorrow", "next Monday", "in 3 days")
- Auto-rescheduling for recurring tasks
- Browser notifications for due tasks
- Priority levels (low, medium, high, urgent)
- Tags and categorization

### User Story 3: Enhanced UI Experience
- Modern responsive layout with header, footer, and sidebar
- Theme system (light, dark, purple) with persistence
- OAuth authentication (Google, Facebook)
- Enhanced login with password strength indicator
- Advanced filtering and sorting (priority, status, tags, due date)
- Mobile-responsive design

## Architecture

### Backend (FastAPI)
```
phase-2-web/backend/
├── app/
│   ├── api/
│   │   ├── v1/endpoints/
│   │   │   ├── chat.py          # AI chat endpoint
│   │   │   ├── notifications.py  # Notification API
│   │   │   ├── preferences.py    # User preferences
│   │   │   └── oauth.py          # OAuth authentication
│   │   └── api_v1/endpoints/
│   │       ├── auth.py           # Email/password auth
│   │       └── tasks.py          # Task CRUD operations
│   ├── models/
│   │   ├── task.py               # Task model with recurrence
│   │   ├── user.py               # User model with OAuth
│   │   └── conversation.py       # Chat history model
│   ├── services/
│   │   ├── recurrence_service.py # Recurring task logic
│   │   ├── notification_service.py # Notification scheduling
│   │   └── scheduler.py          # Background job scheduler
│   ├── utils/
│   │   └── date_parser.py        # Natural language date parsing
│   ├── ai_agent.py               # AI agent orchestration
│   └── config.py                 # Configuration management
├── mcp_server.py                 # MCP server with 6 tools
└── alembic/                      # Database migrations
```

### Frontend (Next.js 14)
```
phase-2-web/frontend/
├── app/
│   ├── api/auth/[...nextauth]/   # NextAuth.js configuration
│   ├── login/                    # Enhanced login page
│   ├── layout.tsx                # Root layout with theme
│   └── themes.css                # Theme CSS variables
├── components/
│   ├── ChatWidget.tsx            # AI chat interface
│   ├── Header.tsx                # Navigation header
│   ├── Footer.tsx                # App footer
│   ├── Sidebar.tsx               # Filter/sort sidebar
│   ├── ThemeToggle.tsx           # Theme switcher
│   └── NotificationPrompt.tsx    # Browser notification prompt
├── context/
│   └── ThemeContext.tsx          # Theme state management
└── lib/
    ├── notifications.ts          # Browser Notification API
    └── useNotifications.ts       # Notification polling hook
```

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLModel**: SQL database ORM with Pydantic integration
- **Alembic**: Database migration tool
- **Anthropic Claude**: Primary AI provider for NLP
- **OpenAI GPT**: Fallback AI provider
- **FastMCP**: Model Context Protocol server
- **APScheduler**: Background job scheduling
- **python-dateutil**: Natural language date parsing
- **PostgreSQL**: Database (Neon DB)

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **NextAuth.js**: Authentication with OAuth
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client
- **React Context API**: State management

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL database (or Neon DB account)
- Anthropic API key or OpenAI API key
- OAuth credentials (optional, for Google/Facebook login)

### Backend Setup

1. **Navigate to backend directory**
```bash
cd phase-2-web/backend
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create `.env` file in `phase-2-web/backend/`:
```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# AI Services (at least one required)
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here

# MCP Server
MCP_SERVER_URL=http://localhost:8001

# JWT Authentication
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OAuth Providers (optional)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
FACEBOOK_CLIENT_ID=your_facebook_client_id
FACEBOOK_CLIENT_SECRET=your_facebook_client_secret
```

5. **Run database migrations**
```bash
alembic upgrade head
```

6. **Start the backend server**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Backend will be available at: `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd phase-2-web/frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment variables**

Create `.env.local` file in `phase-2-web/frontend/`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your_nextauth_secret_here

# OAuth Providers (optional)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
FACEBOOK_CLIENT_ID=your_facebook_client_id
FACEBOOK_CLIENT_SECRET=your_facebook_client_secret
```

4. **Start the development server**
```bash
npm run dev
```

Frontend will be available at: `http://localhost:3000`

### MCP Server (Optional)

To run the MCP server standalone for testing:
```bash
cd phase-2-web/backend
python mcp_server.py
```

MCP server will run on port 8001.

## Usage Guide

### Natural Language Commands

The AI chatbot understands natural language commands:

**Adding tasks:**
- "Add buy groceries tomorrow"
- "Create high priority task finish report"
- "Add weekly meeting every Monday at 10am"
- "New task: Review PR due next Friday"

**Listing tasks:**
- "Show all my tasks"
- "List high priority tasks"
- "What tasks are due this week?"

**Completing tasks:**
- "Mark task complete"
- "Done with buy groceries"
- "Finish the report task"

**Updating tasks:**
- "Change priority to urgent"
- "Update due date to tomorrow"
- "Add tag 'work' to task"

**Deleting tasks:**
- "Delete the groceries task"
- "Remove completed tasks"

### Theme Switching

1. Click the theme toggle in the header
2. Select from: Light, Dark, or Purple theme
3. Theme preference is automatically saved to your account

### Browser Notifications

1. Allow notification permissions when prompted
2. Notifications will appear when tasks are due
3. Notifications check every 5 minutes automatically

### Filtering and Sorting

Use the sidebar to filter tasks by:
- Priority (low, medium, high, urgent)
- Status (pending, in-progress, complete)
- Tags
- Due date range

Sort tasks by:
- Created date
- Due date
- Priority

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login with email/password
- `POST /api/v1/auth/oauth` - OAuth authentication

### Tasks
- `GET /api/v1/tasks` - List tasks with filters
- `POST /api/v1/tasks` - Create new task
- `GET /api/v1/tasks/{id}` - Get task by ID
- `PUT /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task

### AI Chat
- `POST /api/v1/chat` - Process natural language command

### Notifications
- `GET /api/v1/notifications` - Get pending notifications
- `POST /api/v1/notifications/{id}/mark-sent` - Mark notification as sent

### User Preferences
- `PUT /api/v1/user/preferences` - Update user preferences (theme, etc.)

## Testing

### Backend Tests
```bash
cd phase-2-web/backend
pytest
```

### Frontend Tests
```bash
cd phase-2-web/frontend
npm test
```

### MCP Server Verification
```bash
cd phase-2-web/backend
python verify_mcp_server.py
```

## Development

### Database Migrations

Create a new migration:
```bash
cd phase-2-web/backend
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

### Code Quality

Backend linting:
```bash
cd phase-2-web/backend
black .
flake8 .
mypy .
```

Frontend linting:
```bash
cd phase-2-web/frontend
npm run lint
```

## Deployment

### Backend Deployment

1. Set production environment variables
2. Run database migrations
3. Deploy to hosting service (Railway, Render, AWS, etc.)
4. Configure CORS for frontend domain

### Frontend Deployment

1. Set production environment variables
2. Build the application:
```bash
npm run build
```
3. Deploy to Vercel, Netlify, or similar platform

## Troubleshooting

### Database Connection Issues
- Verify DATABASE_URL is correct
- Check database is running and accessible
- Ensure migrations have been applied

### AI Service Errors
- Verify API keys are valid
- Check API rate limits
- Ensure at least one AI provider (Anthropic or OpenAI) is configured

### OAuth Login Issues
- Verify OAuth credentials are correct
- Check redirect URLs are configured in OAuth provider console
- Ensure NEXTAUTH_SECRET is set

### Notification Issues
- Check browser notification permissions
- Verify notification service is running
- Check browser console for errors

## Project Structure

```
hackathon2_todo/
├── phase-1-console/          # Phase 1: Console app
├── phase-2-web/              # Phase 2 & 3: Web app
│   ├── backend/              # FastAPI backend
│   └── frontend/             # Next.js frontend
├── specs/                    # Design specifications
│   ├── phase3-ai-chatbot/    # Phase 3 specs
│   └── ...
└── history/                  # Development history
    ├── prompts/              # Prompt history records
    └── adr/                  # Architecture decision records
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Add tests
4. Run linting and tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Check the troubleshooting section
- Review API documentation at `/docs`
- Check the specs directory for detailed design documents

## Acknowledgments

- Built with Anthropic Claude and OpenAI GPT
- Uses FastMCP for Model Context Protocol
- NextAuth.js for authentication
- Tailwind CSS for styling
