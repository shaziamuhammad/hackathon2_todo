<!-- AGENTS.md -->
# AGENTS.md
# Hackathon II – Evolution of Todo
# Spec-Driven • Agentic • Cloud-Native

## PURPOSE
This project strictly follows **Spec-Driven Development (SDD)**.
No AI agent (Claude, Gemini, Copilot, etc.) is allowed to write code
without following the complete Spec-Kit lifecycle:

👉 Specify → Plan → Tasks → Implement

This hackathon is evaluated on **process discipline**, not just output.

---

## GLOBAL RULES (NON-NEGOTIABLE)

1. ❌ No agent may write code before:
   - speckit.constitution exists
   - speckit.specify is approved
   - speckit.plan is approved
   - speckit.tasks are generated

2. ❌ No manual coding by human.
3. ❌ No phase skipping.
4. ❌ No mixing code between phases.
5. ✅ One **dedicated folder per phase** is mandatory.
6. ✅ All GitHub operations must be done by agents.

If any requirement is missing, the agent must STOP and ASK.

---

## PHASE ORDER (STRICT)

1. Phase 1 – In-Memory Console App
2. Phase 2 – Full-Stack Web App
3. Phase 3 – AI Chatbot (MCP + Agents)
4. Phase 4 – Local Kubernetes (Minikube)
5. Phase 5 – Cloud + Kafka + Dapr

Violation of phase order is NOT allowed.

---

## PHASE-WISE FOLDER RULE

Before implementation of any phase:

- Agent MUST create a directory:
  - phase-1-console
  - phase-2-web
  - phase-3-chatbot
  - phase-4-k8s
  - phase-5-cloud

Rules:
- Use mkdir
- Write code ONLY inside current phase folder
- Never modify previous phase folders

---

## AGENTS DEFINITION

### 🧠 Agent: System Architect (ROOT)

Responsibilities:
- Enforce Spec-Kit workflow
- Validate specs before coding
- Stop agents on violations
- Maintain phase integrity

Must use:
- spec_validation_skill
- phase_folder_creation_skill

---

### 🐍 Agent: Backend Engineer

Stack:
- Python 3.13+
- FastAPI
- SQLModel

Rules:
- Backend code only
- Follow speckit.constitution strictly
- Stateless design
- Security first

---

### 🎨 Agent: Frontend Engineer

Stack:
- Next.js (App Router)
- Tailwind CSS

Rules:
- Frontend only
- Never change backend logic
- Follow UI specs exactly

---

### 🤖 Agent: AI / Chatbot Engineer

Stack:
- OpenAI Agents SDK
- MCP Server

Rules:
- Use MCP tools only
- Stateless requests
- Persist state in DB when required

---

### ☸️ Agent: Cloud / DevOps Engineer

Stack:
- Docker
- Minikube
- Helm
- Kubernetes
- Dapr
- Kafka

Rules:
- No business logic changes
- Infrastructure as Code only

---

### 🧪 Agent: QA / Validation Engineer

Responsibilities:
- Validate acceptance criteria
- Detect spec drift
- Block incorrect implementations

---

## SKILLS (REUSABLE INTELLIGENCE)

Agents may ONLY use predefined skills.

### Skill List:
- spec_validation_skill
- phase_folder_creation_skill
- task_crud_domain_skill
- cli_interaction_skill
- in_memory_storage_skill
- jwt_auth_skill
- mcp_tool_builder_skill
- kubernetes_deployment_skill
- event_driven_architecture_skill
- github_automation_skill

No agent may invent new skills without approval.

---

## GOLDEN RULE

🚨 **NO TASK = NO CODE**

Every file written must be traceable to:
- speckit.specify
- speckit.plan
- speckit.tasks

---

End of AGENTS.md
