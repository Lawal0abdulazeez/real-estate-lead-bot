# IMPLEMENTATION.md

# PrimeHomes Realty — Real Estate Lead Bot
## Implementation Progress & Engineering Log

> **Purpose:** Track what has actually been implemented, how it works, important technical decisions, and the current development state.

---

# 1. Project Status

**Current Phase:** Implementation Preparation  
**Overall Status:** 🟡 Documentation Complete / Development Starting

### Current System State

| Area | Status |
|---|---|
| Requirements | 🟢 Complete |
| PRD | 🟢 Complete |
| Database Design | 🟢 Complete |
| API Specification | 🟢 Complete |
| n8n Specification | 🟢 Complete |
| AI Specification | 🟢 Complete |
| UI/UX Specification | 🟢 Complete |
| Testing Specification | 🟢 Complete |
| Deployment Specification | 🟢 Complete |
| Environment Configuration | ⬜ Pending |
| Backend | ⬜ Not Started |
| Database Implementation | ⬜ Not Started |
| Frontend | ⬜ Not Started |
| n8n Workflows | ⬜ Not Started |
| AI Integration | ⬜ Not Started |
| Lead Qualification | ⬜ Not Started |
| Testing | ⬜ Not Started |
| VPS Deployment | ⬜ Not Started |

---

# 2. Implementation Philosophy

The project follows these principles:

### 1. Simple First

Use the simplest solution that reliably solves the requirement.

### 2. Clear Responsibilities

```text
React
↓
User interface

FastAPI
↓
Application API + business boundaries

PostgreSQL
↓
Source of truth

n8n
↓
Workflow orchestration + integrations

AI
↓
Understanding + extraction + response generation
```

### 3. No Unnecessary Complexity

Do not introduce:

- Microservices
- Kubernetes
- Message brokers
- Complex event architectures
- Multiple databases
- Unnecessary abstraction layers

unless the actual system requires them.

### 4. AI Does Not Own Business Rules

AI can interpret information.

The application determines what is valid and what should happen.

---

# 3. Architecture

Current target architecture:

```text
                         CUSTOMER
                            │
                            ▼
                         REACT
                            │
                            ▼
                         FASTAPI
                       /         \
                      /           \
                     ▼             ▼
               POSTGRESQL         N8N
                                   │
                         ┌─────────┼─────────┐
                         ▼         ▼         ▼
                        AI     NOTIFY     SHEETS
```

---

# 4. Implementation Progress

## Phase 1 — Requirements

### Status: 🟢 Complete

Completed:

- Business problem defined
- Product goal defined
- Customer workflow defined
- Sales workflow defined
- Lead information defined
- Lead qualification requirements defined
- MVP scope defined

---

# 5. Phase 2 — System Documentation

### Status: 🟢 Complete

Completed documentation:

- [x] PRD
- [x] Database Design
- [x] API Specification
- [x] n8n Workflow Specification
- [x] AI Specification
- [x] UI/UX Specification
- [x] README
- [x] Development Setup
- [x] Lead Qualification Specification
- [x] Testing Specification
- [x] Deployment Specification

Pending:

- [ ] Environment Configuration
- [ ] Operations Runbook

---

# 6. Phase 3 — Project Foundation

### Status: ⬜ Not Started

Target structure:

```text
real-estate-lead-bot/
│
├── frontend/
├── backend/
├── n8n/
├── database/
├── tests/
├── docs/
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── docker-compose.prod.yml
└── README.md
```

### Implementation Log

**Status:** ⬜

**Completed:**
- None

**Files Created:**
- None

**Tests:**
- None

**Notes:**
- Repository structure will be created before application development.

**Next:**
- Create project structure.

---

# 7. Phase 4 — Database

### Status: ⬜ Not Started

### Target Technology

PostgreSQL

### Primary Tables

```text
users
roles
leads
conversations
messages
lead_scores
lead_assignments
follow_ups
activities
integration_syncs
```

### Implementation Order

1. Database connection
2. SQLAlchemy models
3. Alembic
4. Initial migration
5. Seed data
6. Database tests

### Implementation Log

**Status:** ⬜

**Models Implemented:**
- None

**Migrations:**
- None

**Tests:**
- None

**Notes:**
- PostgreSQL will remain the primary source of truth.

---

# 8. Phase 5 — FastAPI Backend

### Status: ⬜ Not Started

### Initial API

```text
GET    /api/v1/health

POST   /api/v1/auth/login

POST   /api/v1/leads
GET    /api/v1/leads
GET    /api/v1/leads/{id}
PATCH  /api/v1/leads/{id}

POST   /api/v1/conversations
GET    /api/v1/conversations/{id}

POST   /api/v1/messages
GET    /api/v1/conversations/{id}/messages

POST   /api/v1/leads/{id}/qualify

POST   /api/v1/follow-ups
GET    /api/v1/follow-ups
PATCH  /api/v1/follow-ups/{id}
```

### Implementation Order

1. FastAPI application
2. Configuration
3. Database connection
4. Health endpoint
5. Models
6. Schemas
7. Repository layer
8. Services
9. Lead API
10. Conversation API
11. Message API
12. Authentication
13. Follow-up API

### Implementation Log

**Status:** ⬜

**Endpoints Implemented:**
- None

**Tests:**
- None

**Notes:**
- FastAPI owns API access and business boundaries.

---

# 9. Phase 6 — React Frontend

### Status: ⬜ Not Started

## Customer Interface

Target:

```text
Customer
   ↓
Chat Interface
   ↓
Send Message
   ↓
FastAPI
   ↓
Bot Response
```

### Components

- Chat window
- Message list
- Message input
- Send button
- Loading state
- Typing indicator
- Error state
- Retry action

## Sales Dashboard

Components:

- Dashboard
- Lead list
- Lead filters
- Lead details
- Conversation history
- Score
- Classification
- Status
- Assignment
- Follow-ups
- Activity timeline

### Implementation Log

**Status:** ⬜

**Pages Implemented:**
- None

**Components Implemented:**
- None

**Tests:**
- None

---

# 10. Phase 7 — n8n

### Status: ⬜ Not Started

## Workflow 1

`PRH-LEAD-PROCESS-MESSAGE`

Target:

```text
Webhook
 ↓
Validate
 ↓
Check Idempotency
 ↓
Fetch Context
 ↓
AI Extraction
 ↓
Validate AI Output
 ↓
Merge Lead Data
 ↓
Check Missing Fields
 ↓
Qualify
 ↓
Generate Response
 ↓
Save Response
 ↓
Return Response
```

## Workflow 2

`PRH-LEAD-QUALIFY`

```text
Receive Lead
 ↓
Apply Scoring Rules
 ↓
Calculate Score
 ↓
Classify
 ↓
Save Score
 ↓
Update Lead
```

## Workflow 3

`PRH-LEAD-NOTIFY-SALES`

```text
HOT Lead
 ↓
Retrieve Lead
 ↓
Create Notification
 ↓
Notify Sales
 ↓
Record Activity
```

## Workflow 4

`PRH-FOLLOWUP-REMINDER`

```text
Due Follow-Up
 ↓
Retrieve Lead
 ↓
Send Reminder
 ↓
Update Follow-Up
 ↓
Record Activity
```

### Implementation Log

**Status:** ⬜

**Workflows Created:**
- None

**Tests:**
- None

**Notes:**
- n8n orchestrates workflows; it does not become the application's source of truth.

---

# 11. Phase 8 — AI

### Status: ⬜ Not Started

## Extraction

The AI must extract:

```json
{
  "intent": "BUY",
  "transaction_type": "BUY",
  "property_type": "APARTMENT",
  "bedrooms": 3,
  "location": "Lekki",
  "budget_min": null,
  "budget_max": 80000000,
  "currency": "NGN",
  "timeline": "WITHIN_3_MONTHS",
  "customer_name": null,
  "email": null,
  "phone": null,
  "confidence": 0.96
}
```

## AI Responsibilities

- Understand customer message
- Extract lead information
- Classify intent
- Detect missing information
- Generate clarification questions
- Generate customer responses
- Summarize conversations
- Detect human handoff requirements

## AI Non-Responsibilities

AI must not:

- Authenticate users
- Authorize users
- Write directly to PostgreSQL
- Decide database integrity rules
- Assign sales ownership directly
- Invent property availability
- Invent prices
- Confirm bookings without system verification

### Implementation Log

**Status:** ⬜

**Model:**
- TBD

**Prompt Versions:**
- None

**Evaluation Dataset:**
- Not created

**Tests:**
- None

---

# 12. Phase 9 — Lead Qualification

### Status: ⬜ Not Started

## Score

Maximum:

```text
Intent               20
Property Requirement 15
Location              15
Budget                20
Timeline              20
Contact               10
-------------------------
TOTAL                100
```

## Classification

```text
80–100 → HOT
60–79  → WARM
30–59  → COLD
0–29   → UNQUALIFIED
```

### Implementation Rule

AI extracts the information.

The deterministic qualification logic calculates the score.

```text
AI
 ↓
Structured Data
 ↓
Validation
 ↓
Qualification Service
 ↓
Score
 ↓
Classification
```

### Implementation Log

**Status:** ⬜

**Scoring Service:**
- Not implemented

**Tests:**
- None

---

# 13. Phase 10 — Testing

### Status: ⬜ Not Started

Testing will be implemented alongside development rather than waiting until the end.

## Backend

- [ ] Unit tests
- [ ] API tests
- [ ] Validation tests
- [ ] Authentication tests

## AI

- [ ] Extraction tests
- [ ] Intent tests
- [ ] Missing-field tests
- [ ] Human-handoff tests
- [ ] Failure tests

## n8n

- [ ] Workflow success
- [ ] Duplicate events
- [ ] AI failure
- [ ] API failure
- [ ] Notification failure

## Frontend

- [ ] Chat tests
- [ ] Error tests
- [ ] Lead dashboard tests

## E2E

- [ ] Complete customer journey
- [ ] HOT lead journey
- [ ] Incomplete lead journey
- [ ] Human handoff journey

---

# 14. Phase 11 — Deployment

### Status: ⬜ Not Started

Target environment:

```text
ONE VPS
│
├── Nginx
├── React
├── FastAPI
├── PostgreSQL
└── n8n
```

Deployment stack:

- Ubuntu LTS
- Docker
- Docker Compose
- Nginx
- HTTPS
- PostgreSQL volumes
- n8n persistent storage

### Implementation Log

**VPS:** Not provisioned

**Domain:** Not configured

**Docker:** Not configured

**Nginx:** Not configured

**HTTPS:** Not configured

**Backups:** Not configured

---

# 15. End-to-End Implementation Status

Target flow:

```text
CUSTOMER
   ↓
REACT
   ↓
FASTAPI
   ↓
N8N
   ↓
AI
   ↓
EXTRACTION
   ↓
VALIDATION
   ↓
LEAD DATABASE
   ↓
QUALIFICATION
   ↓
SCORE
   ↓
CLASSIFICATION
   ↓
CUSTOMER RESPONSE
   ↓
SALES NOTIFICATION
```

Current status:

```text
Customer
   ↓
React                 ⬜
   ↓
FastAPI               ⬜
   ↓
n8n                   ⬜
   ↓
AI                    ⬜
   ↓
Extraction            ⬜
   ↓
Validation            ⬜
   ↓
Database              ⬜
   ↓
Qualification         ⬜
   ↓
Score                 ⬜
   ↓
Response              ⬜
   ↓
Sales Notification    ⬜
```

---

# 16. Engineering Decisions Log

Record important decisions here so future developers or AI agents understand why the system was built this way.

## Decision 001 — PostgreSQL as Source of Truth

**Decision:** PostgreSQL is the authoritative database.

**Reason:** The application requires reliable relational data, relationships, transactions, querying, and lead history.

**Alternative:** Google Sheets

**Reason rejected:** Sheets is useful for operational reporting but should not be the primary application database.

---

## Decision 002 — n8n for Workflow Orchestration

**Decision:** n8n handles automation and integrations.

**Reason:** It is well suited for connecting AI, notifications, Google Sheets, scheduled workflows, and external services.

**Boundary:** FastAPI remains responsible for application business boundaries.

---

## Decision 003 — FastAPI for Backend

**Decision:** FastAPI is the main application API.

**Reason:** It provides a clean Python API layer for validation, authentication, database access, and custom business logic.

---

## Decision 004 — AI Does Not Directly Write to Database

**Decision:** AI output must pass through application validation before persistence.

**Reason:** AI output is probabilistic and should not control database integrity.

---

## Decision 005 — VPS Deployment

**Decision:** Start with a single VPS.

**Reason:** The expected MVP workload does not justify Kubernetes, multiple servers, or microservices.

---

# 17. Implementation Change Log

Use this section for meaningful changes.

| Date | Change | Reason | Status |
|---|---|---|---|
| 2026-09-03 | Initial implementation tracker created | Track project development | 🟢 |
| | | | |
| | | | |

---

# 18. Current Sprint

## Sprint Goal

> Establish the project foundation and begin implementing the backend/database.

### Tasks

- [ ] Create repository structure
- [ ] Create `.env.example`
- [ ] Set up Python environment
- [ ] Set up FastAPI
- [ ] Set up PostgreSQL
- [ ] Create database configuration
- [ ] Create first models
- [ ] Configure Alembic
- [ ] Create initial migration
- [ ] Implement `/health`
- [ ] Add first backend tests

### Sprint Status

**🟡 Not Started**

---

# 19. Current Task

**Task:** Project Foundation

**Status:** ⬜ Not Started

**Objective:**

Create the initial repository structure and development environment without implementing unnecessary application functionality.

**Expected Result:**

```text
real-estate-lead-bot/
├── frontend/
├── backend/
├── n8n/
├── database/
├── tests/
├── docs/
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

**Next Task:**

Database setup.

---

# 20. How to Update This File

After completing a task, update:

### Status

```text
⬜ Not Started
🟡 In Progress
🟢 Completed
🔴 Blocked
⏸️ On Hold
```

### Implementation Record

For every meaningful task, record:

```text
Task:
Status:
Objective:
Implementation:
Files Changed:
Tests:
Issues:
Decision:
Next:
```

Example:

```text
Task:
Create FastAPI health endpoint

Status:
🟢 Completed

Objective:
Provide a simple endpoint for checking API availability.

Implementation:
Added GET /api/v1/health.

Files Changed:
backend/app/main.py
backend/app/api/v1/health.py
tests/test_health.py

Tests:
Health endpoint returns HTTP 200.

Issues:
None.

Next:
Implement database connection.
```

---

# 21. AI Coding Agent Instructions

Before modifying the project, an AI coding agent should:

1. Read `README.md`.
2. Read the relevant specification.
3. Read `TASK.md`.
4. Read this file.
5. Identify the current task.
6. Inspect the existing implementation.
7. Make the smallest required change.
8. Run relevant tests.
9. Report files changed.
10. Update this implementation tracker.
11. Update `TASK.md`.
12. Do not redesign the architecture without a documented reason.

### Important

Do not mark a task as complete simply because code was written.

A task is complete only when:

```text
Implementation
+
Validation
+
Relevant Tests
+
Documentation Update
```

are complete.

---

# 22. Definition of Done

A feature is considered implemented when:

- [ ] Requirement is understood
- [ ] Implementation exists
- [ ] Relevant validation exists
- [ ] Relevant tests pass
- [ ] Errors are handled
- [ ] Documentation is updated
- [ ] `TASK.md` is updated
- [ ] `IMPLEMENTATION.md` is updated
- [ ] No unnecessary architecture was introduced

---

# 23. Final Project Principle

> **Build → Test → Document → Update → Move to the next task.**

The goal is not to produce a large codebase.

The goal is to produce a **simple, reliable, maintainable Real Estate Lead Bot** that solves the actual business problem.