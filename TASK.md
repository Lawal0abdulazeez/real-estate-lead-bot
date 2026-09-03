# TASK.md

# PrimeHomes Realty — Real Estate Lead Bot
## Project Task Tracker

> **Purpose:** Track all development tasks required to build, test, and deploy the Real Estate Lead Bot.

---

## 1. Project Status

**Overall Status:** 🟡 Planning / Documentation Complete  
**Current Phase:** Implementation Preparation  
**MVP Status:** Not yet implemented

### Status Legend

- ⬜ Not Started
- 🟡 In Progress
- 🟢 Completed
- 🔴 Blocked
- ⏸️ On Hold

---

# 2. Development Roadmap

```text
DOCUMENTATION
     ↓
PROJECT SETUP
     ↓
DATABASE
     ↓
BACKEND API
     ↓
FRONTEND
     ↓
N8N AUTOMATION
     ↓
AI PROCESSING
     ↓
LEAD QUALIFICATION
     ↓
SALES DASHBOARD
     ↓
TESTING
     ↓
VPS DEPLOYMENT
     ↓
MVP COMPLETE
```

---

# 3. Documentation

## Requirements

- [x] Define business problem
- [x] Define product goal
- [x] Define target users
- [x] Define MVP scope
- [x] Define success criteria
- [x] Define core customer information
- [x] Define property information
- [x] Define customer intent
- [x] Define lead qualification requirements

## System Documentation

- [x] PRD
- [x] Database design
- [x] API specification
- [x] n8n workflow specification
- [x] AI specification
- [x] UI/UX specification
- [x] README
- [x] Development setup
- [x] Lead qualification specification
- [x] Testing specification
- [x] Deployment specification
- [ ] Environment configuration
- [ ] Operations runbook
- [ ] Implementation tracker

---

# 4. Project Foundation

## Repository

- [ ] Create project repository
- [ ] Create initial branch structure
- [ ] Create `.gitignore`
- [ ] Create `.env.example`
- [ ] Create README
- [ ] Create documentation folders
- [ ] Create frontend directory
- [ ] Create backend directory
- [ ] Create n8n directory
- [ ] Create database directory
- [ ] Create tests directory

## Development Environment

- [ ] Install Node.js
- [ ] Install Python
- [ ] Create Python virtual environment
- [ ] Install backend dependencies
- [ ] Install frontend dependencies
- [ ] Install/configure PostgreSQL
- [ ] Configure n8n
- [ ] Configure environment variables
- [ ] Verify all services locally

---

# 5. Database

## PostgreSQL Setup

- [ ] Create PostgreSQL database
- [ ] Configure database connection
- [ ] Create SQLAlchemy models
- [ ] Configure Alembic
- [ ] Create initial migration
- [ ] Run migration successfully
- [ ] Create seed data

## Core Tables

- [ ] `users`
- [ ] `roles`
- [ ] `leads`
- [ ] `conversations`
- [ ] `messages`
- [ ] `lead_scores`
- [ ] `lead_assignments`
- [ ] `follow_ups`
- [ ] `activities`
- [ ] `integration_syncs`

## Database Validation

- [ ] Test relationships
- [ ] Test constraints
- [ ] Test indexes
- [ ] Test timestamps
- [ ] Test UUID generation
- [ ] Test duplicate message prevention
- [ ] Test migrations

---

# 6. FastAPI Backend

## Project Setup

- [ ] Create FastAPI application
- [ ] Configure application settings
- [ ] Configure database connection
- [ ] Configure logging
- [ ] Configure CORS
- [ ] Configure API versioning
- [ ] Add health endpoint

## Authentication

- [ ] Implement login
- [ ] Implement JWT authentication
- [ ] Implement password hashing
- [ ] Implement role handling
- [ ] Protect internal endpoints

## Lead APIs

- [ ] `POST /api/v1/leads`
- [ ] `GET /api/v1/leads`
- [ ] `GET /api/v1/leads/{id}`
- [ ] `PATCH /api/v1/leads/{id}`
- [ ] Lead status update
- [ ] Lead assignment
- [ ] Lead qualification endpoint
- [ ] Lead filtering
- [ ] Lead search
- [ ] Lead pagination

## Conversation APIs

- [ ] Create conversation
- [ ] Get conversation
- [ ] Get conversation messages
- [ ] Create customer message
- [ ] Create bot message
- [ ] Message processing status
- [ ] Message idempotency

## Follow-Up APIs

- [ ] Create follow-up
- [ ] Get follow-ups
- [ ] Update follow-up
- [ ] Complete follow-up
- [ ] Cancel follow-up

## Activity APIs

- [ ] Create activity
- [ ] Get activity history
- [ ] Track assignment
- [ ] Track status changes

---

# 7. React Frontend

## Customer Interface

- [ ] Create React application
- [ ] Create customer layout
- [ ] Build chat interface
- [ ] Build message component
- [ ] Build message input
- [ ] Add send functionality
- [ ] Add loading state
- [ ] Add typing indicator
- [ ] Add failed-message state
- [ ] Add retry functionality
- [ ] Add conversation persistence

## Lead Information

- [ ] Display extracted customer information
- [ ] Display property requirements
- [ ] Display lead status where appropriate
- [ ] Add optional lead form
- [ ] Add progressive information collection

## Sales Dashboard

- [ ] Dashboard layout
- [ ] Lead list
- [ ] Lead search
- [ ] Lead filtering
- [ ] Lead sorting
- [ ] Lead details
- [ ] Conversation history
- [ ] Lead score display
- [ ] Lead classification display
- [ ] Lead status update
- [ ] Lead assignment
- [ ] Follow-up management
- [ ] Activity timeline

---

# 8. n8n Automation

## Core Workflow

### `PRH-LEAD-PROCESS-MESSAGE`

- [ ] Create webhook
- [ ] Authenticate webhook
- [ ] Validate incoming event
- [ ] Check idempotency
- [ ] Retrieve lead context
- [ ] Retrieve conversation history
- [ ] Send message to AI
- [ ] Validate AI output
- [ ] Merge extracted information
- [ ] Check missing information
- [ ] Trigger qualification
- [ ] Generate response
- [ ] Save response
- [ ] Return/send response

## Qualification Workflow

### `PRH-LEAD-QUALIFY`

- [ ] Receive lead data
- [ ] Apply scoring rules
- [ ] Calculate score
- [ ] Determine classification
- [ ] Save score history
- [ ] Update lead

## Sales Notification

### `PRH-LEAD-NOTIFY-SALES`

- [ ] Detect HOT lead
- [ ] Retrieve lead details
- [ ] Generate notification
- [ ] Send notification
- [ ] Record notification activity

## Follow-Up

### `PRH-FOLLOWUP-REMINDER`

- [ ] Detect due follow-ups
- [ ] Retrieve lead
- [ ] Send reminder
- [ ] Update follow-up status
- [ ] Record activity

## Google Sheets

### `PRH-SHEET-SYNC-LEAD`

- [ ] Create Google Sheet structure
- [ ] Configure authentication
- [ ] Create lead sync
- [ ] Handle updates
- [ ] Handle sync failures
- [ ] Prevent duplicate rows

## Error Handling

### `PRH-ERROR-HANDLER`

- [ ] Capture workflow errors
- [ ] Record error details
- [ ] Notify administrator where necessary
- [ ] Support retry
- [ ] Prevent customer data loss

---

# 9. AI

## AI Extraction

- [ ] Implement intent extraction
- [ ] Implement transaction type extraction
- [ ] Implement property type extraction
- [ ] Implement bedroom extraction
- [ ] Implement location extraction
- [ ] Implement budget extraction
- [ ] Implement timeline extraction
- [ ] Implement name extraction
- [ ] Implement email extraction
- [ ] Implement phone extraction
- [ ] Implement confidence score

## AI Response

- [ ] Create response-generation prompt
- [ ] Create clarification-question prompt
- [ ] Create human-handoff behavior
- [ ] Add conversation context
- [ ] Prevent unsupported claims
- [ ] Add fallback response

## AI Reliability

- [ ] Validate structured output
- [ ] Handle invalid AI output
- [ ] Handle AI timeout
- [ ] Handle AI failure
- [ ] Add retry strategy
- [ ] Version prompts
- [ ] Create evaluation dataset
- [ ] Run regression tests

---

# 10. Lead Qualification

## Scoring

- [ ] Implement intent score
- [ ] Implement property requirement score
- [ ] Implement location score
- [ ] Implement budget score
- [ ] Implement timeline score
- [ ] Implement contact information score

## Classification

- [ ] Implement HOT
- [ ] Implement WARM
- [ ] Implement COLD
- [ ] Implement UNQUALIFIED

## Validation

- [ ] Test score = 0
- [ ] Test score = 100
- [ ] Test classification boundaries
- [ ] Test score recalculation
- [ ] Test score reasons
- [ ] Test incomplete leads

---

# 11. Customer Experience

- [ ] Customer sends message
- [ ] Message appears immediately
- [ ] Backend receives message
- [ ] AI processes message
- [ ] Lead information is extracted
- [ ] Missing information is identified
- [ ] Bot asks useful clarification
- [ ] Lead is stored
- [ ] Lead is scored
- [ ] Customer receives response
- [ ] Sales team receives HOT lead notification
- [ ] Sales agent can view lead
- [ ] Sales agent can follow up

---

# 12. Testing

## Backend

- [ ] Health endpoint test
- [ ] Authentication tests
- [ ] Lead creation test
- [ ] Lead retrieval test
- [ ] Lead update test
- [ ] Message creation test
- [ ] Validation tests
- [ ] Authorization tests

## Database

- [ ] Model tests
- [ ] Relationship tests
- [ ] Constraint tests
- [ ] Migration tests
- [ ] Transaction tests

## AI

- [ ] BUY scenario
- [ ] RENT scenario
- [ ] LAND scenario
- [ ] Missing information
- [ ] Human-agent request
- [ ] Unclear message
- [ ] Ambiguous budget
- [ ] Hallucination prevention

## n8n

- [ ] Successful workflow
- [ ] Invalid input
- [ ] Duplicate event
- [ ] AI failure
- [ ] Database/API failure
- [ ] Notification failure
- [ ] Google Sheets failure

## Frontend

- [ ] Send message
- [ ] Receive response
- [ ] Loading state
- [ ] Error state
- [ ] Retry
- [ ] Lead list
- [ ] Lead details
- [ ] Lead update

## End-to-End

- [ ] Complete customer journey
- [ ] HOT lead journey
- [ ] Incomplete lead journey
- [ ] Human handoff journey
- [ ] Failed AI journey

---

# 13. VPS Deployment

## Server

- [ ] Provision VPS
- [ ] Install Ubuntu LTS
- [ ] Create deploy user
- [ ] Configure SSH
- [ ] Install Docker
- [ ] Install Docker Compose
- [ ] Configure firewall

## Application

- [ ] Clone repository
- [ ] Configure production `.env`
- [ ] Build frontend
- [ ] Build backend
- [ ] Configure PostgreSQL
- [ ] Configure n8n
- [ ] Configure Docker volumes
- [ ] Run migrations
- [ ] Start services

## Nginx

- [ ] Configure domain
- [ ] Configure API subdomain
- [ ] Configure n8n subdomain
- [ ] Configure reverse proxy
- [ ] Configure HTTPS
- [ ] Configure SSL renewal

## Production Validation

- [ ] Frontend accessible
- [ ] API accessible
- [ ] Database connected
- [ ] n8n accessible
- [ ] AI processing works
- [ ] Customer message works
- [ ] Sales notification works
- [ ] Google Sheets sync works
- [ ] Backups configured
- [ ] VPS restart tested

---

# 14. MVP Definition of Done

The MVP is complete when a customer can:

```text
Send Message
     ↓
React
     ↓
FastAPI
     ↓
n8n
     ↓
AI
     ↓
Extract Requirements
     ↓
Store Lead
     ↓
Calculate Score
     ↓
Classify Lead
     ↓
Generate Response
     ↓
Notify Sales if Required
```

And the sales team can:

- [ ] View the lead
- [ ] View conversation
- [ ] View extracted requirements
- [ ] View score
- [ ] View classification
- [ ] View/update status
- [ ] Take follow-up action

---

# 15. Current Priority

## 🔥 Next Tasks

1. [ ] Create `ENVIRONMENT_CONFIG.md`
2. [ ] Create `OPERATIONS_RUNBOOK.md`
3. [ ] Create initial repository structure
4. [ ] Set up backend
5. [ ] Set up PostgreSQL
6. [ ] Create database models
7. [ ] Create first migration
8. [ ] Implement FastAPI health endpoint
9. [ ] Implement lead API
10. [ ] Implement conversation/message API

---

# 16. Agentic Development Rule

When using an AI coding agent:

1. Read the relevant documentation first.
2. Check this task file before starting work.
3. Pick one task or a small related group.
4. Implement only that scope.
5. Run the relevant tests.
6. Update `IMPLEMENTATION.md`.
7. Mark the completed task here.
8. Do not silently change architecture.
9. Do not introduce unnecessary technologies.
10. If a requirement is unclear, stop and document the question before making a major assumption.

---

# 17. Task Completion Format

When completing a task, update:

```text
Task:
Status:
Implementation:
Files Changed:
Tests:
Notes:
Next Task:
```

---

# 18. Current Project Principle

> Build the simplest reliable system that solves the business problem.

Do not add technology, abstraction, infrastructure, or complexity unless there is a clear reason for it.