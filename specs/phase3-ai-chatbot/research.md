# Research Findings: AI-Powered Todo Chatbot

**Feature**: AI-Powered Todo Chatbot
**Date**: 2026-02-08

## MCP Server Implementation

### Decision: FastMCP Library Selection
**Rationale**: FastMCP is chosen for its simplicity and Pythonic approach to MCP server implementation. It provides a lightweight framework for exposing functions as standardized tools for AI agents.
**Alternatives considered**:
- Official MCP SDK
- Custom MCP implementation

### Decision: Tool Exposure Strategy
**Rationale**: Exposing existing CRUD functions as MCP tools enables the AI agent to interact with the todo system through standardized interfaces.
**Tools to be exposed**:
- add_task(title, description, priority, due_date, recurrence)
- delete_task(task_id)
- update_task(task_id, title, description, priority, due_date, recurrence, status)
- list_tasks(filter_params)
- mark_complete(task_id)

## AI Model Selection

### Decision: Anthropic Model Preference
**Rationale**: Following the requirement to prefer Anthropic models for free tier usage, Claude models will be used as the primary AI provider with OpenAI as fallback.
**Fallback strategy**: If Anthropic models are unavailable or exceed free tier limits, the system will fall back to OpenAI GPT models.

## Backend Architecture

### Decision: FastAPI Extension
**Rationale**: Extending the existing FastAPI backend with new endpoints maintains consistency and leverages existing infrastructure.
**Integration approach**: New `/api/chat` endpoint will connect to AI agent which uses MCP tools.

## Frontend Integration

### Decision: ChatWidget Update
**Rationale**: Updating the existing ChatWidget.tsx to connect to the new `/api/chat` endpoint preserves existing UI while enabling AI functionality.
**Changes needed**: Replace direct API calls with chat endpoint calls.

## Advanced Feature Implementation

### Decision: Recurring Task Handling
**Rationale**: Recurring tasks will be implemented with a recurrence pattern field and a background job scheduler.
**Implementation**: Store recurrence patterns and use cron-like scheduling for auto-generation.

### Decision: Due Date and Priority Processing
**Rationale**: Natural language processing for dates and priorities requires specific extraction and validation.
**Approach**: Use datetime libraries for date parsing and predefined priority levels (low, medium, high, urgent).

## UI Enhancement Strategy

### Decision: Theme Implementation
**Rationale**: CSS variables and theme providers will enable dynamic switching between purple/light-dark themes.
**Implementation**: React context for theme management with CSS custom properties.

### Decision: Authentication Enhancement
**Rationale**: NextAuth.js provides robust support for multiple authentication providers including Google, Facebook, and email/password.
**Implementation**: NextAuth.js integration with social providers and custom password validation UI.