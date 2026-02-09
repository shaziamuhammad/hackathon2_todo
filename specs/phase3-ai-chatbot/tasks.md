---
description: "Task list for AI-Powered Todo Chatbot implementation"
---

# Tasks: AI-Powered Todo Chatbot

**Input**: Design documents from `/specs/phase3-ai-chatbot/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api.yaml

**Tests**: Tests are NOT explicitly requested in the specification, so test tasks are omitted.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `phase-2-web/backend/`
- **Frontend**: `phase-2-web/frontend/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency installation

- [X] T001 Add fastmcp dependency to phase-2-web/backend/requirements.txt or pyproject.toml
- [X] T002 [P] Add anthropic SDK dependency to phase-2-web/backend/requirements.txt or pyproject.toml
- [X] T003 [P] Add openai SDK dependency to phase-2-web/backend/requirements.txt or pyproject.toml
- [X] T004 [P] Add python-dateutil dependency for date parsing to phase-2-web/backend/requirements.txt or pyproject.toml
- [X] T005 [P] Add next-auth dependency to phase-2-web/frontend/package.json
- [X] T006 Install backend dependencies using pip install -r requirements.txt
- [X] T007 Install frontend dependencies using npm install in phase-2-web/frontend/
- [X] T008 Create .env.example file in phase-2-web/backend/ with required environment variables (ANTHROPIC_API_KEY, OPENAI_API_KEY, MCP_SERVER_URL)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T009 Extend TodoItem model in phase-2-web/backend/models.py to add recurrence_pattern field (JSON type)
- [X] T010 [P] Extend TodoItem model in phase-2-web/backend/models.py to add tags field (array type)
- [X] T011 [P] Extend TodoItem model in phase-2-web/backend/models.py to add due_date field (datetime type)
- [X] T012 [P] Extend User model in phase-2-web/backend/models.py to add theme_preference field (enum: light, dark, purple)
- [X] T013 [P] Extend User model in phase-2-web/backend/models.py to add provider and provider_id fields for OAuth
- [X] T014 Create Conversation model in phase-2-web/backend/models.py with user_id, messages array, timestamps
- [X] T015 Create database migration script for new fields in phase-2-web/backend/migrations/ or alembic/
- [ ] T016 Run database migrations to update schema in Neon DB
- [X] T017 Create phase-2-web/backend/config.py to load environment variables (API keys, MCP server URL)
- [X] T018 Create phase-2-web/backend/utils/date_parser.py for natural language date parsing using python-dateutil

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural Language Todo Management (Priority: P1) 🎯 MVP

**Goal**: Enable users to manage todos using natural language commands through an AI chatbot

**Independent Test**: Send natural language commands to /api/chat endpoint and verify that todo operations (add, update, delete, mark complete, list) are executed correctly in the database

### MCP Server Implementation for User Story 1

- [X] T019 [P] [US1] Create phase-2-web/backend/mcp_server.py with FastMCP server initialization
- [X] T020 [P] [US1] Implement add_task MCP tool in phase-2-web/backend/mcp_server.py that wraps existing CRUD function
- [X] T021 [P] [US1] Implement delete_task MCP tool in phase-2-web/backend/mcp_server.py with user ownership verification
- [X] T022 [P] [US1] Implement update_task MCP tool in phase-2-web/backend/mcp_server.py supporting all task properties
- [X] T023 [P] [US1] Implement list_tasks MCP tool in phase-2-web/backend/mcp_server.py with filtering and sorting
- [X] T024 [P] [US1] Implement mark_complete MCP tool in phase-2-web/backend/mcp_server.py with status validation
- [X] T025 [US1] Add MCP server startup script and configuration in phase-2-web/backend/mcp_server.py
- [ ] T026 [US1] Test MCP server by running it standalone on port 8001 and verifying tool exposure

### AI Agent Integration for User Story 1

- [X] T027 [US1] Create phase-2-web/backend/ai_agent.py with Anthropic client initialization
- [X] T028 [US1] Implement MCP tool connection logic in phase-2-web/backend/ai_agent.py to connect to MCP server URL
- [X] T029 [US1] Implement natural language processing function in phase-2-web/backend/ai_agent.py to interpret user commands
- [X] T030 [US1] Implement tool orchestration logic in phase-2-web/backend/ai_agent.py to map intents to MCP tool calls
- [X] T031 [US1] Implement response formatting in phase-2-web/backend/ai_agent.py to generate user-friendly responses
- [X] T032 [US1] Add OpenAI fallback logic in phase-2-web/backend/ai_agent.py when Anthropic is unavailable
- [X] T033 [US1] Implement conversation context management in phase-2-web/backend/ai_agent.py using Conversation model

### Chat Endpoint for User Story 1

- [X] T034 [US1] Create POST /api/chat endpoint in phase-2-web/backend/main.py or routes/chat.py
- [X] T035 [US1] Implement request validation for ChatRequest schema in phase-2-web/backend/main.py
- [X] T036 [US1] Integrate ai_agent.py with /api/chat endpoint to process natural language input
- [X] T037 [US1] Implement response formatting for ChatResponse schema in phase-2-web/backend/main.py
- [X] T038 [US1] Add error handling for AI processing failures in phase-2-web/backend/main.py
- [X] T039 [US1] Add authentication middleware to /api/chat endpoint in phase-2-web/backend/main.py

### Frontend Chat Integration for User Story 1

- [X] T040 [US1] Update phase-2-web/frontend/src/components/ChatWidget.tsx to call /api/chat endpoint instead of direct API calls
- [X] T041 [US1] Implement message sending logic in phase-2-web/frontend/src/components/ChatWidget.tsx with POST request to /api/chat
- [X] T042 [US1] Implement response display logic in phase-2-web/frontend/src/components/ChatWidget.tsx to show AI responses
- [X] T043 [US1] Add typing indicator in phase-2-web/frontend/src/components/ChatWidget.tsx while waiting for AI response
- [X] T044 [US1] Implement conversation history display in phase-2-web/frontend/src/components/ChatWidget.tsx
- [X] T045 [US1] Add error handling and user feedback in phase-2-web/frontend/src/components/ChatWidget.tsx for failed requests

**Checkpoint**: At this point, User Story 1 should be fully functional - users can manage todos using natural language commands

---

## Phase 4: User Story 2 - Advanced Todo Features (Priority: P2)

**Goal**: Enable users to create recurring tasks, set due dates, and receive browser notifications

**Independent Test**: Create recurring tasks and tasks with due dates through the chatbot, verify auto-rescheduling works, and confirm browser notifications are delivered at specified times

### Advanced Parsing in AI Agent for User Story 2

- [X] T046 [P] [US2] Extend phase-2-web/backend/ai_agent.py to parse recurring task patterns (daily, weekly, monthly, yearly)
- [X] T047 [P] [US2] Extend phase-2-web/backend/ai_agent.py to parse due dates from natural language using date_parser.py
- [X] T048 [P] [US2] Extend phase-2-web/backend/ai_agent.py to parse priority levels from natural language
- [X] T049 [US2] Update tool orchestration in phase-2-web/backend/ai_agent.py to pass recurrence_pattern to add_task tool
- [X] T050 [US2] Update tool orchestration in phase-2-web/backend/ai_agent.py to pass due_date to add_task tool

### Recurring Task Logic for User Story 2

- [X] T051 [US2] Create phase-2-web/backend/services/recurrence_service.py to handle recurring task logic
- [X] T052 [US2] Implement auto-reschedule function in phase-2-web/backend/services/recurrence_service.py to generate next occurrence
- [X] T053 [US2] Create background job scheduler in phase-2-web/backend/services/scheduler.py using APScheduler or similar
- [X] T054 [US2] Integrate recurrence_service.py with scheduler.py to auto-generate recurring tasks
- [X] T055 [US2] Update mark_complete MCP tool in phase-2-web/backend/mcp_server.py to trigger auto-reschedule for recurring tasks

### Notification System for User Story 2

- [X] T056 [US2] Create phase-2-web/backend/services/notification_service.py to manage notification scheduling
- [X] T057 [US2] Implement notification scheduling logic in phase-2-web/backend/services/notification_service.py based on due_date
- [X] T058 [US2] Create GET /api/notifications endpoint in phase-2-web/backend/main.py to retrieve pending notifications
- [X] T059 [US2] Implement browser notification API integration in phase-2-web/frontend/src/utils/notifications.ts
- [X] T060 [US2] Add notification permission request in phase-2-web/frontend/src/components/NotificationPrompt.tsx
- [X] T061 [US2] Implement notification polling or WebSocket connection in phase-2-web/frontend/src/hooks/useNotifications.ts
- [X] T062 [US2] Display browser notifications when tasks are due in phase-2-web/frontend/src/utils/notifications.ts

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - users can create recurring tasks and receive notifications

---

## Phase 5: User Story 3 - Enhanced UI Experience (Priority: P3)

**Goal**: Provide improved UI with header, footer, sidebar, theme options, and enhanced authentication

**Independent Test**: Verify that header, footer, and sidebar are displayed correctly, theme switching works, and OAuth login options are functional

### Layout Enhancements for User Story 3

- [X] T063 [P] [US3] Create phase-2-web/frontend/src/components/Header.tsx with navigation and user profile
- [X] T064 [P] [US3] Create phase-2-web/frontend/src/components/Footer.tsx with app information and links
- [X] T065 [P] [US3] Create phase-2-web/frontend/src/components/Sidebar.tsx with filter options (priority, status, tags, due date)
- [X] T066 [US3] Update phase-2-web/frontend/src/app/layout.tsx to include Header, Footer, and Sidebar components
- [X] T067 [US3] Implement responsive layout in phase-2-web/frontend/src/app/layout.tsx for mobile and desktop views

### Theme System for User Story 3

- [X] T068 [US3] Create phase-2-web/frontend/src/contexts/ThemeContext.tsx for theme state management
- [X] T069 [US3] Implement theme provider in phase-2-web/frontend/src/contexts/ThemeContext.tsx with purple, light, and dark modes
- [X] T070 [US3] Create phase-2-web/frontend/src/styles/themes.css with CSS variables for purple, light, and dark themes
- [X] T071 [US3] Create phase-2-web/frontend/src/components/ThemeToggle.tsx component for theme selection
- [X] T072 [US3] Integrate ThemeToggle component in Header.tsx in phase-2-web/frontend/src/components/Header.tsx
- [X] T073 [US3] Persist theme preference to backend by updating User model via API in phase-2-web/frontend/src/contexts/ThemeContext.tsx
- [X] T074 [US3] Create PUT /api/user/preferences endpoint in phase-2-web/backend/main.py to save theme preference

### Enhanced Authentication for User Story 3

- [ ] T075 [US3] Configure NextAuth.js in phase-2-web/frontend/src/app/api/auth/[...nextauth]/route.ts
- [ ] T076 [US3] Add Google OAuth provider configuration in phase-2-web/frontend/src/app/api/auth/[...nextauth]/route.ts
- [ ] T077 [US3] Add Facebook OAuth provider configuration in phase-2-web/frontend/src/app/api/auth/[...nextauth]/route.ts
- [ ] T078 [US3] Update phase-2-web/frontend/src/app/login/page.tsx to add OAuth login buttons (Google, Facebook)
- [ ] T079 [US3] Implement password visibility toggle in phase-2-web/frontend/src/app/login/page.tsx
- [ ] T080 [US3] Add character length indicator for password field in phase-2-web/frontend/src/app/login/page.tsx
- [ ] T081 [US3] Add password strength indicator in phase-2-web/frontend/src/app/login/page.tsx
- [ ] T082 [US3] Update backend authentication in phase-2-web/backend/auth.py to handle OAuth tokens from NextAuth.js
- [ ] T083 [US3] Create POST /api/auth/oauth endpoint in phase-2-web/backend/main.py to verify OAuth tokens

### Sidebar Filtering and Sorting for User Story 3

- [X] T084 [US3] Implement filter state management in phase-2-web/frontend/src/components/Sidebar.tsx
- [X] T085 [US3] Add priority filter UI in phase-2-web/frontend/src/components/Sidebar.tsx
- [X] T086 [US3] Add status filter UI in phase-2-web/frontend/src/components/Sidebar.tsx
- [X] T087 [US3] Add tag filter UI in phase-2-web/frontend/src/components/Sidebar.tsx
- [X] T088 [US3] Add due date filter UI in phase-2-web/frontend/src/components/Sidebar.tsx
- [X] T089 [US3] Add sort options UI in phase-2-web/frontend/src/components/Sidebar.tsx (by due_date, priority, created_at)
- [X] T090 [US3] Connect Sidebar filters to task list display in phase-2-web/frontend/src/components/TaskList.tsx
- [X] T091 [US3] Update GET /api/tasks endpoint calls to include filter and sort parameters from Sidebar

**Checkpoint**: All user stories should now be independently functional - complete UI with chatbot, advanced features, and enhanced authentication

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T092 [P] Add comprehensive error handling across all backend endpoints in phase-2-web/backend/main.py
- [ ] T093 [P] Add logging for all AI agent operations in phase-2-web/backend/ai_agent.py
- [ ] T094 [P] Add logging for all MCP tool calls in phase-2-web/backend/mcp_server.py
- [ ] T095 [P] Optimize database queries in phase-2-web/backend/crud.py for list_tasks with filters
- [ ] T096 [P] Add input validation for all API endpoints in phase-2-web/backend/main.py
- [ ] T097 [P] Add rate limiting to /api/chat endpoint in phase-2-web/backend/main.py to prevent abuse
- [ ] T098 [P] Update phase-2-web/frontend/src/components/ChatWidget.tsx styling to match purple theme
- [ ] T099 [P] Add loading states for all async operations in phase-2-web/frontend/src/components/
- [ ] T100 [P] Add accessibility attributes (ARIA labels) to all UI components in phase-2-web/frontend/src/components/
- [ ] T101 Update README.md with setup instructions from quickstart.md
- [ ] T102 Create API documentation from contracts/api.yaml in docs/api.md
- [ ] T103 Run quickstart.md validation to ensure all setup steps work correctly
- [ ] T104 Verify all success criteria from spec.md are met (95% accuracy, 3-second response time, etc.)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User Story 1 (Phase 3): Can start after Foundational - No dependencies on other stories
  - User Story 2 (Phase 4): Can start after Foundational - Extends US1 but independently testable
  - User Story 3 (Phase 5): Can start after Foundational - Independent of US1/US2
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Extends AI agent from US1 but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Completely independent of US1/US2

### Within Each User Story

**User Story 1**:
- MCP Server tools (T020-T024) can run in parallel
- AI Agent implementation (T027-T033) depends on MCP server being functional
- Chat endpoint (T034-T039) depends on AI agent being functional
- Frontend updates (T040-T045) depend on chat endpoint being functional

**User Story 2**:
- Advanced parsing (T046-T048) can run in parallel
- Recurring task logic (T051-T055) is independent
- Notification system (T056-T062) is independent

**User Story 3**:
- Layout components (T063-T065) can run in parallel
- Theme system (T068-T074) is independent
- Authentication (T075-T083) is independent
- Sidebar filtering (T084-T091) depends on layout components

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T002, T003, T004, T005)
- All Foundational model extensions marked [P] can run in parallel (T010, T011, T012, T013)
- All MCP tools marked [P] can run in parallel (T020, T021, T022, T023, T024)
- All advanced parsing tasks marked [P] can run in parallel (T046, T047, T048)
- All layout components marked [P] can run in parallel (T063, T064, T065)
- All Polish tasks marked [P] can run in parallel (T092-T100)
- Once Foundational phase completes, all three user stories can start in parallel (if team capacity allows)

---

## Parallel Example: User Story 1 - MCP Tools

```bash
# Launch all MCP tool implementations together:
Task T020: "Implement add_task MCP tool in phase-2-web/backend/mcp_server.py"
Task T021: "Implement delete_task MCP tool in phase-2-web/backend/mcp_server.py"
Task T022: "Implement update_task MCP tool in phase-2-web/backend/mcp_server.py"
Task T023: "Implement list_tasks MCP tool in phase-2-web/backend/mcp_server.py"
Task T024: "Implement mark_complete MCP tool in phase-2-web/backend/mcp_server.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T008)
2. Complete Phase 2: Foundational (T009-T018) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 (T019-T045)
4. **STOP and VALIDATE**: Test User Story 1 independently by sending natural language commands
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP - Natural language todo management!)
3. Add User Story 2 → Test independently → Deploy/Demo (Advanced features - recurring tasks, notifications!)
4. Add User Story 3 → Test independently → Deploy/Demo (Enhanced UI - themes, OAuth, filters!)
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T018)
2. Once Foundational is done:
   - Developer A: User Story 1 (T019-T045) - Core chatbot
   - Developer B: User Story 2 (T046-T062) - Advanced features
   - Developer C: User Story 3 (T063-T091) - UI enhancements
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- MCP server runs on port 8001, main backend on port 8000
- Frontend runs on port 3000 (Next.js default)
- All file paths are relative to project root
- Environment variables must be configured before running
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
