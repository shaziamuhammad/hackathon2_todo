---
id: 2
title: "AI-Powered Todo Chatbot Planning"
stage: plan
date_iso: 2026-02-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: ai-todo-chatbot
branch: "1-ai-todo-chatbot"
user: user
command: "/sp.plan"
labels: ["planning", "architecture", "ai", "mcp", "todo"]
link_spec: "specs/phase3-ai-chatbot/spec.md"
link_ticket: null
link_adr: null
link_pr: null
files_yaml: |
  - specs/phase3-ai-chatbot/plan.md
  - specs/phase3-ai-chatbot/research.md
  - specs/phase3-ai-chatbot/data-model.md
  - specs/phase3-ai-chatbot/contracts/api.yaml
  - specs/phase3-ai-chatbot/quickstart.md
tests_yaml: |
  - "Constitution compliance check"
  - "Architecture design validation"
  - "Data model verification"
outcome: |
  Successfully created comprehensive implementation plan for AI-powered Todo Chatbot
  including detailed architecture, phases, and technical specifications.
evaluation: |
  The plan addresses all requirements from the user input and aligns with
  project constitution principles. All necessary design artifacts created.
---

# Prompt History Record: AI-Powered Todo Chatbot Planning

## User Input (PROMPT_TEXT)
```
Project: Phase 3 - AI-Powered Todo Chatbot (using OpenAI Agents SDK + MCP)

Goal: Implement AI-powered Todo management chatbot with minimum and advanced features as per hackathon requirements. This will integrate with the existing project structure, where Phase 1 and Phase 2 have been completed, with a FastAPI backend (tasks.py with CRUD), Next.js frontend (ChatWidget.tsx), and Neon DB.

Technical Plan:

Key Decisions:

MCP Server Setup: Use FastMCP (install with pip install fastmcp) for a simple and Pythonic MCP server.

Exposing Backend CRUD Functions: Expose at least the following as MCP tools:

add_task, delete_task, update_task, list_tasks, mark_complete from the existing tasks.py file in the backend.

Advanced Parsing: The agent should be able to handle parsing of:

Recurring tasks (weekly/monthly).

Due dates.

Priorities.

Search/filter/sort functionalities.

Backend Updates:

Create or update mcp.py to initialize and run the MCP server.

Add the /api/chat endpoint in main.py to process requests from the frontend.

AI Agent Setup:

Create or update ai-agent/agent.py to connect to the MCP server URL (provided via environment variables).

Use Anthropic or OpenAI API for the AI-powered agent to process natural language requests.

Frontend Updates:

ChatWidget.tsx: Update to call the /api/chat backend endpoint and handle responses from the agent.

Browser notifications: Implement notifications for reminders and task updates.

UI Updates:

layout.tsx: Add a header, footer, and sidebar for sorting and filtering tasks. Implement purple/light-dark themes and animations.

login/page.tsx: Add options for Google/Facebook/email login with a toggle for showing passwords and a character length indicator.

Task Breakdown:

Backend:

Step 1: Install FastMCP and set up MCP server:

Install with pip install fastmcp.

Create mcp.py in the backend folder.

Set up MCP tools for the existing CRUD operations from tasks.py.

Step 2: Implement the /api/chat endpoint in main.py:

Ensure the endpoint connects with the AI agent (via MCP).

Step 3: Set up environment variables for the MCP URL and API keys (OpenAI/Anthropic).

Step 4: Update tasks.py to handle advanced features (recurring tasks, due dates, priorities).

AI Agent:

Step 5: Create or update ai-agent/agent.py:

Implement functions for connecting to the MCP server and handling requests.

Integrate OpenAI/Anthropic for natural language processing (NLP) tasks.

Frontend:

Step 6: Update ChatWidget.tsx:

Integrate the frontend with the new /api/chat backend endpoint.

Handle responses from the backend to display appropriate messages and reminders.

Step 7: Implement browser notifications for reminders and task completions.

UI Updates:

Step 8: Update layout.tsx:

Add header, footer, sidebar, and task filters.

Implement purple and light-dark themes, with animations where appropriate.

Step 9: Update login/page.tsx:

Add OAuth login options (Google/Facebook/email).

Include password toggle and character length indicator.

Integration Testing:

Step 10: Test the MCP server with the /api/chat endpoint.

Step 11: Test task CRUD operations via the MCP tools.

Step 12: Test the frontend integration (UI, notifications, and agent responses).

Step 13: Verify all features work as expected (add/edit/delete tasks, search/filter, recurring tasks).

Deployment:

Step 14: Deploy the application on Vercel (for frontend) and the backend on a cloud server (e.g., AWS or Heroku).

Step 15: Ensure that all components (MCP server, agent, frontend, and backend) are connected and functioning correctly in the production environment.

Output: Write this technical plan to specs/phase3-ai-chatbot/plan.md, detailing the tasks and steps required for implementation.
```

## Assistant Response (RESPONSE_TEXT)
Created comprehensive implementation plan for the AI-Powered Todo Chatbot including:

- Updated technical context with research findings
- Constitution compliance check ensuring adherence to project principles
- Detailed architecture with components and technology stack
- Four-phase implementation approach (Research & Preparation, MCP Server & Backend, AI Agent Logic, Frontend Enhancement, Testing)
- Risk assessment with mitigation strategies
- Success metrics aligned with feature requirements

Additionally created supporting artifacts:
- research.md with technology decisions and rationale
- data-model.md with entity definitions and relationships
- contracts/api.yaml with OpenAPI specification
- quickstart.md with setup and development guidelines

All deliverables specified in the user input have been completed and documented in the implementation plan.

## Next Steps
Proceed to task breakdown with `/sp.tasks` to create actionable implementation tasks based on this plan.