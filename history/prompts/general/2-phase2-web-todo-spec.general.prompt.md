---
id: 2
title: phase2-web-todo-spec
stage: spec
date: 2026-02-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: phase2-web
branch: main
user: claude
command: sp.specify
labels: ["specification", "todo-app", "authentication", "security"]
links:
  spec: specs/phase2-web/spec.md
  ticket: null
  adr: null
  pr: null
files_yaml:
  - specs/phase2-web/spec.md
  - specs/phase2-web/checklists/requirements.md
tests_yaml:
  - "Specification completeness check"
  - "Requirements validation"
  - "Quality checklist verification"
prompt_text: |
  Create Phase 2 spec at specs/phase2-web/spec.md.

  Must implement Hackathon Phase II requirements:
  - Stack: Next.js 16+ App Router (TypeScript + Tailwind), FastAPI (Python), SQLModel, Neon Postgres, Better Auth.
  - Auth: signup/signin using Better Auth; Better Auth must issue JWT.
  - Security: Every backend endpoint requires Authorization: Bearer <token>. Backend verifies JWT using BETTER_AUTH_SECRET and extracts user_id. If missing/invalid token -> 401. If URL user_id != token user_id -> 403.
  - Data isolation: each user only sees/modifies own tasks.
  - Required REST endpoints EXACTLY:
    GET /api/{user_id}/tasks
    POST /api/{user_id}/tasks
    GET /api/{user_id}/tasks/{id}
    PUT /api/{user_id}/tasks/{id}
    DELETE /api/{user_id}/tasks/{id}
    PATCH /api/{user_id}/tasks/{id}/complete
  - UI: responsive, modern dashboard with good visual hierarchy, empty states, loading states, error states.
  - Validation: title required, description optional.
  Include clear acceptance criteria + edge cases.
response_text: |
  Successfully created comprehensive specification for Phase 2 Web Todo Application with:
  - Detailed functional requirements covering authentication, security, API endpoints, and UI
  - User scenarios and testing scenarios defined
  - Success criteria with quantitative and qualitative measures
  - Complete entity definitions and system constraints
  - Clear scope definition (in/out of scope)
  - Quality checklist validation completed
outcome: |
  Specification document created at specs/phase2-web/spec.md with all required elements included. Ready for planning phase.
evaluation: |
  The specification comprehensively covers all requirements from the user input with appropriate detail level for development planning.
---