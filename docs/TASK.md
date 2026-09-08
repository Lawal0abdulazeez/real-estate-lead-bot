# TASK.md

# PrimeHomes Realty — Real Estate Lead Bot
## Project Task Tracker

> **Purpose:** Track all development tasks required to build, test, and deploy the Real Estate Lead Bot.

---

## 1. Project Status

**Overall Status:** 🟡 Core backend + frontend MVP implemented  
**Current Phase:** Local testing with n8n  
**MVP Status:** Partial — chat → API → DB → n8n trigger works

### Status Legend

- ⬜ Not Started
- 🟡 In Progress
- 🟢 Completed
- 🔴 Blocked
- ⏸️ On Hold

---

# 2. Development Roadmap

```text
DOCUMENTATION          🟢
PROJECT SETUP          🟢
DATABASE MODELS        🟢 (core tables)
BACKEND API            🟢 (health, leads, conversations, messages, qualify)
FRONTEND               🟢 (chat + leads list, orange/yellow UI)
N8N AUTOMATION         🟡 (webhook trigger from backend ready — configure workflows)
AI PROCESSING          ⬜
LEAD QUALIFICATION     🟢 (deterministic scorer)
SALES DASHBOARD        🟡 (basic list)
TESTING                🟡
VPS DEPLOYMENT         ⬜
```

---

# 4. Project Foundation

- [x] Repository structure, .gitignore, .env.example, docker-compose
- [x] FastAPI skeleton + health
- [x] Frontend Vite React scaffold

---

# 5. Database

- [x] SQLAlchemy models: leads, conversations, messages, lead_scores, activities
- [x] Enums matching specs
- [x] Alembic env + create_tables helper
- [ ] Run initial migration on your machine
- [ ] Seed data (optional)

---

# 6. FastAPI Backend

- [x] Health endpoint
- [x] Lead CRUD + list/filter
- [x] POST /leads/{id}/qualify
- [x] Conversation create/get
- [x] Message create + list
- [x] n8n webhook trigger on customer message
- [x] Deterministic qualification service
- [ ] Auth / JWT (later)
- [ ] Follow-up APIs (later)

---

# 7. React Frontend

- [x] Vite + React + TS
- [x] Orange / yellow modern palette
- [x] Customer chat page (create conversation, send message, poll for bot reply)
- [x] Leads list page
- [ ] Lead detail / conversation history view
- [ ] Auth screens

---

# 15. Current Priority

1. [x] Backend models + core APIs
2. [x] Frontend chat + leads
3. [ ] You: start Postgres + backend + frontend locally
4. [ ] You: point n8n webhook at the MESSAGE_RECEIVED event
5. [ ] Wire AI extraction inside n8n and call back FastAPI to update lead + bot message

---

# 18. Current Project Principle

> Build the simplest reliable system that solves the business problem.
